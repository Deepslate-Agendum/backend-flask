import hashlib, uuid

import user.dao as user_dao

def get(user_id: int = None) -> list | None:
    """Get a user by ID, or all users if no ID is given."""

    if user_id is not None:
        return user_dao.get_by_id(user_id)
    else:
        return user_dao.get_all()

def hash_password(salted_password: str) -> str:
    """Return the hash for a password that has been salted."""
    return hashlib.sha256(salted_password.encode()).hexdigest()

def generate_salt() -> str:
    """Generate a random salt."""
    return str(uuid.uuid4())

def create(username: str = None, password: str = None) -> int:
    """Create a new user."""
    if user_dao.get_by_username(username):
        return -1

    salt = generate_salt()
    return user_dao.create(username, hash_password(password + salt), salt)

def update(user_id: int, username: str = None, password: str = None) -> bool:
    """Update a user given its ID."""
    if not user_dao.get_by_id(user_id):
        return False

    salt = user_dao.get_salt(user_id)
    return user_dao.update(user_id, username, hash_password(password + salt))

def delete(user_id: int) -> bool:
    """Delete a user given its ID."""
    if not user_dao.get_by_id(user_id):
        return False

    return user_dao.delete(user_id)