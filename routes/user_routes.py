from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import logging

user_blueprint = Blueprint('user_routes', __name__)

@user_blueprint.route('/manage')
def manage_users():
    """Displays a list of all users."""
    # Ensure that the user is logged in and has an Admin role
    if 'user_id' not in session or session.get('role') != 1:  # 1 is assumed to be the Admin role
        flash("You must be an admin to view this page.", "danger")
        return redirect(url_for('auth_routes.login'))  # Redirect to login if not logged in or not an admin

    # Fetch all users from the database
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.*, r.role_name 
        FROM users u 
        JOIN roles r ON u.role_id = r.role_id
        ORDER BY u.created_at DESC;
    """)
    users = cursor.fetchall()
    cursor.close()
    con.close()

    return render_template('users/manage_users.html', users=users)

from flask import request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from db import get_db_connection  # Ensure this function exists

@user_blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    """Handles adding a new user."""
    
    # Ensure only admins (role_id = 1) can add users
    if 'user_id' not in session or session.get('role') != 1:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth_routes.login'))

    # Establish DB connection
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    # ✅ Fetch available roles from the database
    cursor.execute("SELECT role_id, role_name FROM roles")  
    roles = cursor.fetchall()  # Get the roles list
    cursor.close()
    con.close()

    # Handle form submission
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form.get('role_id')

        # Ensure role ID is provided
        if not role_id:
            flash("Role is required.", "danger")
            return render_template('users/add_user.html', roles=roles)

        # Hash the password before storing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        con = get_db_connection()
        cursor = con.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (user_firstname, user_lastname, user_email, user_password, role_id, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW());
            """, (first_name, last_name, email, hashed_password, role_id))
            con.commit()
            flash("User added successfully!", "success")
            return redirect(url_for('user_routes.manage_users'))  # Redirect to manage users page

        except Exception as e:
            con.rollback()
            flash(f"Error adding user: {e}", "danger")
        finally:
            cursor.close()
            con.close()

    return render_template('users/add_user.html', roles=roles)  # ✅ Pass roles to the template

@user_blueprint.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Handles editing an existing user."""
    if 'user_id' not in session or session.get('role') != 1:  # Only Admins can edit users
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth_routes.login'))  # Redirect to login if not an admin

    # Fetch the user details for the user to edit
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('user_routes.manage_users'))  # Redirect if user does not exist

    # Handle form submission to update the user
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role_id = request.form['role_id']

        try:
            cursor.execute("""
                UPDATE users
                SET user_firstname = %s, user_lastname = %s, user_email = %s, role_id = %s
                WHERE user_id = %s;
            """, (first_name, last_name, email, role_id, user_id))
            con.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for('user_routes.manage_users'))  # Redirect to manage users page
        except Exception as e:
            con.rollback()
            flash(f"Error updating user: {e}", "danger")
        finally:
            cursor.close()
            con.close()

    # Fetch roles to display in the dropdown
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT role_id, role_name FROM roles ORDER BY role_name;")
    roles = cursor.fetchall()
    cursor.close()
    con.close()

    return render_template('users/edit_user.html', user=user, roles=roles)  # Render the edit user form

@user_blueprint.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Deletes a user (Admin Only)."""
    
    # Ensure only admins can delete users
    if 'user_id' not in session or session.get('role') != 1:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth_routes.login'))

    con = get_db_connection()
    cursor = con.cursor()

    try:
        # Check if user exists before deleting
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            flash("User not found.", "warning")
            return redirect(url_for('user_routes.manage_users'))

        # Delete user
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        con.commit()

        flash("User deleted successfully!", "success")
        logging.info(f"User {user_id} deleted successfully.")
    
    except Exception as e:
        con.rollback()
        logging.error(f"Error deleting user {user_id}: {e}")
        flash(f"Error deleting user: {e}", "danger")

    finally:
        cursor.close()
        con.close()

    return redirect(url_for('user_routes.manage_users'))  # Redirect after deletion
