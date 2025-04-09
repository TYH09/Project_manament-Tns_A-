"""
This file  Handles storing, retrieving, and clearing sessions.
"""
from flask import session

class SessionManager:
    @staticmethod
    def set_user_session(user):
        """
        Stores user details in the session after login.
        """
        session['user_id'] = user['user_id']
        session['user_name'] = f"{user['user_firstname']} {user['user_lastname']}"
        session['role'] = user['role_id']
    
    @staticmethod
    def get_user():
        """
        Retrieves the current logged-in user's details from session.
        """
        return {
            "user_id": session.get('user_id'),
            "user_name": session.get('user_name'),
            "role": session.get('role')
        }
    
    @staticmethod
    def clear_session():
        """
        Logs out the user by clearing the session.
        """
        session.clear()
