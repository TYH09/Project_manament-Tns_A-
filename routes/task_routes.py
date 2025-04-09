from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

# ✅ Define task blueprint
task_blueprint = Blueprint('task_routes', __name__)

### ✅ Add Task Route
@task_blueprint.route('/projects/<int:project_id>/tasks/add', methods=['GET', 'POST'])
def add_task(project_id):
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    # Check if project exists
    cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
    project = cursor.fetchone()
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for('project_routes.manage_projects'))

    # Fetch users to assign tasks to
    cursor.execute("SELECT user_id, user_firstname, user_lastname FROM users")
    users = cursor.fetchall()

    if request.method == 'POST':
        task_title = request.form['task_title']
        task_description = request.form['task_description']
        assigned_to = request.form['assigned_to'] if request.form['assigned_to'] else None
        due_date = request.form['due_date'] if request.form['due_date'] else None
        status = request.form['status']

        try:
            cursor.execute("""
                INSERT INTO tasks (project_id, task_title, task_description, assigned_to, due_date, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW());
            """, (project_id, task_title, task_description, assigned_to, due_date, status))
            con.commit()
            flash("Task added successfully!", "success")
            return redirect(url_for('task_routes.view_tasks', project_id=project_id))  # ✅ Redirect to task list
        except Exception as err:
            con.rollback()
            flash(f"Database error: {err}", "danger")
        finally:
            cursor.close()
            con.close()

    return render_template('tasks/add_task.html', project=project, users=users)


### ✅ View Task List for a Project
@task_blueprint.route('/projects/<int:project_id>/tasks')
def view_tasks(project_id):
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    # Fetch the project
    cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
    project = cursor.fetchone()
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for('project_routes.manage_projects'))

    # Fetch tasks for this project
    cursor.execute("""
        SELECT t.*, CONCAT(u.user_firstname, ' ', u.user_lastname) AS assigned_to_name
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.user_id
        WHERE t.project_id = %s
        ORDER BY t.created_at DESC;
    """, (project_id,))
    tasks = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template('tasks/task_list.html', project=project, tasks=tasks)


### ✅ Delete Task Route
@task_blueprint.route('/projects/<int:project_id>/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(project_id, task_id):
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('auth_routes.login'))

    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE task_id = %s AND project_id = %s", (task_id, project_id))
        con.commit()
        flash("Task deleted successfully!", "success")
    except Exception as err:
        con.rollback()
        flash(f"Database error: {err}", "danger")
    finally:
        cursor.close()
        con.close()

    return redirect(url_for('task_routes.view_tasks', project_id=project_id))
