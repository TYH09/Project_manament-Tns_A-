"""
This file provides helper functions related to session timeouts, security checks, and validation.
"""

from flask import session, redirect, url_for, flash

def login_required(f):
    """
    A decorator that checks if a user is logged in before allowing access to a route.
    """
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper
