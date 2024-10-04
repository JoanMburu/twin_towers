from flask import request, abort

VALID_ADMIN_TOKENS = {
    "admin-token-123",
    "admin-token-456"
}

def authenticate_admin():
    """Check if the request contains a valid admin token."""
    token = request.headers.get('Authorization')

    if not token:
        abort(403, description="Admin access required")

    token = token.replace("Bearer ", "")

    if token not in VALID_ADMIN_TOKENS:
        abort(403, description="Invalid admin token")
    
    return True 