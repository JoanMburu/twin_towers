from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

def authenticate_admin():
    """Decorator to check if the user is an admin."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return
    return wrapper
