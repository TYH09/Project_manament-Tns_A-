
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
from email.mime.text import MIMEText
from db import get_db_connection
from config import Config

auth_blueprint = Blueprint('auth_routes', __name__)

@auth_blueprint.route('/')
def index():
    """Handles the root URL and displays projects."""
    if 'user_id' not in session:
        flash("Please log in to view your projects.", "info")
        return redirect(url_for('auth_routes.login'))

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.project_id, p.project_name, p.project_description
        FROM projects p
        WHERE p.created_by = %s
        ORDER BY p.due_date;
    """, (session.get('user_id'),))
    projects = cursor.fetchall()
    cursor.close()
    con.close()
    return render_template('dashboard/home.html', projects=projects)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = get_db_connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        con.close()

        if user and check_password_hash(user['user_password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = f"{user['user_firstname']} {user['user_lastname']}"
            session['role'] = user['role_id']
            flash("Login successful!", "success")
            return redirect(url_for('auth_routes.home'))
        else:
            flash("Invalid email or password. Please try again.", "danger")
    return render_template('auth/login.html')
@auth_blueprint.route('/home')
def home():
    """Displays the home page."""
    if 'user_id' not in session:
        flash("Please log in to continue.", "info")
        return redirect(url_for('auth_routes.login'))
    
    return render_template('dashboard/home.html', user_name=session.get('user_name'))

@auth_blueprint.route('/dashboard')
def dashboard():
    """Logged-in landing page."""
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))

    # ✅ Safely get session values to avoid KeyError
    user_name = session.get('user_name', 'Unknown User')
    role = session.get('role', 'Guest')

    return render_template('dashboard/dashboard.html', user_name=user_name, role=role)
@auth_blueprint.route('/logout')
def logout():
    """Handles user logout."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth_routes.login'))

@auth_blueprint.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    """Allows users to request a password reset."""
    if request.method == 'POST':
        email = request.form['email']
        con = get_db_connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (email,))
        user = cursor.fetchone()

        if user:
            reset_token = secrets.token_urlsafe(32)
            cursor.execute("UPDATE users SET reset_token = %s WHERE user_email = %s;", (reset_token, email))
            con.commit()

            try:
                send_reset_email(email, reset_token)
                flash("Password reset link has been sent to your email.", "success")
            except Exception as e:
                flash(f"Error sending email: {str(e)}", "danger")
        else:
            flash("No account found with that email.", "danger")
        cursor.close()
        con.close()
    return render_template('auth/password_reset.html')

@auth_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Allows users to reset their password using a token."""
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT user_email FROM users WHERE reset_token = %s", (token,))
    user = cursor.fetchone()

    if not user:
        flash("Invalid or expired reset token.", "danger")
        return redirect(url_for('auth_routes.password_reset'))

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

        cursor.execute("UPDATE users SET user_password = %s, reset_token = NULL WHERE reset_token = %s;", (hashed_password, token))
        con.commit()
        flash("Your password has been reset successfully!", "success")
        return redirect(url_for('auth_routes.login'))
    
    cursor.close()
    con.close()
    return render_template('auth/reset_password.html', token=token)

def send_reset_email(email, token):
    """Sends a password reset email with a unique link."""
    reset_url = url_for('auth_routes.reset_password', token=token, _external=True)
    message = f"Click the link below to reset your password:\n\n{reset_url}"

    msg = MIMEText(message)
    msg['Subject'] = "Password Reset Request"
    msg['From'] = Config.MAIL_USERNAME
    msg['To'] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False