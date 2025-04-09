from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

project_blueprint = Blueprint('project_routes', __name__)

### ✅ Manage Projects Route
from flask import request

@project_blueprint.route('/projects/manage')
def manage_projects():
    """Displays a list of all projects."""
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))

    # Get page number from request args, default to 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of projects per page

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    # Get total count of projects
    cursor.execute("SELECT COUNT(*) AS total FROM projects")
    total_projects = cursor.fetchone()['total']
    
    # Calculate total pages
    total_pages = (total_projects // per_page) + (1 if total_projects % per_page > 0 else 0)

    # Fetch paginated projects
    offset = (page - 1) * per_page
    cursor.execute("""
        SELECT p.project_id, p.project_name, p.project_description, p.category, p.due_date,
               CONCAT(u.user_firstname, ' ', u.user_lastname) AS created_by, p.created_at
        FROM projects p
        JOIN users u ON p.created_by = u.user_id
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s;
    """, (per_page, offset))
    projects = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template('projects/projectpage.html', projects=projects, page=page, total_pages=total_pages)

### ✅ Add Project Route
@project_blueprint.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    """Handles adding a new project."""
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))  # Corrected

    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        category = request.form['category']
        due_date = request.form['due_date'] if request.form['due_date'] else None
        created_by = session['user_id']  # Automatically assign logged-in user

        con = get_db_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO projects (project_name, project_description, category, due_date, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW());
            """, (project_name, project_description, category, due_date, created_by))
            con.commit()
            flash("Project added successfully!", "success")
            return redirect(url_for('project_routes.manage_projects'))  # Corrected
        except Exception as err:
            con.rollback()
            flash(f"Database error: {err}", "danger")
        finally:
            cursor.close()
            con.close()

    return render_template('projects/add_project.html')

### ✅ Edit Project Route
@project_blueprint.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    """Handles editing an existing project."""
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))  # Corrected

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.close()
    con.close()

    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for('project_routes.manage_projects'))  # Corrected

    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        category = request.form['category']
        due_date = request.form['due_date'] if request.form['due_date'] else None

        con = get_db_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE projects
                SET project_name = %s, project_description = %s, category = %s, due_date = %s
                WHERE project_id = %s;
            """, (project_name, project_description, category, due_date, project_id))
            con.commit()
            flash("Project updated successfully!", "success")
            return redirect(url_for('project_routes.manage_projects'))  # Corrected
        except Exception as err:
            con.rollback()
            flash(f"Database error: {err}", "danger")
        finally:
            cursor.close()
            con.close()

    return render_template('projects/edit_project.html', project=project)

### ✅ Delete Project Route
@project_blueprint.route('/projects/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    """Deletes a project."""
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))  # Corrected

    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
        con.commit()
        flash("Project deleted successfully!", "success")
    except Exception as err:
        con.rollback()
        flash(f"Database error: {err}", "danger")
    finally:
        cursor.close()
        con.close()

    return redirect(url_for('project_routes.manage_projects'))  # Corrected
