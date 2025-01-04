from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from flask import jsonify
from typing import Callable, Any

def role_required(role: str) -> Callable:
    """
    Decorator to enforce role-based access control.

    Args:
        role (str): The required role to access the route.

    Returns:
        Callable: The decorated function.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            verify_jwt_in_request()  # Ensure the request has a valid JWT
            claims = get_jwt()  # Get the JWT claims
            if claims.get("role") != role:
                return jsonify({"error": "Unauthorized"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator

def get_current_user_id() -> int:
    """
    Returns the user ID from the JWT token.

    Returns:
        int: The ID of the currently logged-in user.
    """
    verify_jwt_in_request()  # Ensure the request has a valid JWT
    return get_jwt_identity()

def get_current_user_role() -> str:
    """
    Returns the user role from the JWT token.

    Returns:
        str: The role of the currently logged-in user.
    """
    verify_jwt_in_request()  # Ensure the request has a valid JWT
    return get_jwt().get("role")

def admin_required(fn: Callable) -> Callable:
    """
    Decorator to enforce admin role-based access control.

    Args:
        fn (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    return role_required("admin")(fn)

def supervisor_required(fn: Callable) -> Callable:
    """
    Decorator to enforce supervisor role-based access control.

    Args:
        fn (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    return role_required("supervisor")(fn)

def student_required(fn: Callable) -> Callable:
    """
    Decorator to enforce student role-based access control.

    Args:
        fn (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    return role_required("student")(fn)