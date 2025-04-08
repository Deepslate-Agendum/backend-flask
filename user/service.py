from typing import Optional, List, Tuple

import hashlib
import uuid

import user.dao as user_dao
import user_token.service as token_service
from db_python_util.db_classes import User

def get(user_id: str = None) -> List[User] | Optional[User]:
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

def create(username: str, password: str) -> Optional[str]:
    """Create a new user."""
    salt = generate_salt()
    return user_dao.create(username, hash_password(password + salt), salt)

def update(user_id: str, username: str, password: str):
    """Update a user given its ID."""
    user = user_dao.get_by_id(user_id)

    salt = user.password_salt
    user_dao.update(user_id, username, hash_password(password + salt))

def delete(user_id: str):
    """Delete a user given its ID."""
    if user_dao.get_by_id(user_id) is None:
        return False

    return user_dao.delete(user_id)

def login(username: str, password: str) -> Optional[Tuple[User, str]]:
    user = user_dao.get_by_username(username)
    # TODO: please note that this fails if the user isn't found, this is assuming AGENDUM-62 gets merged
    password_hash = hash_password(password + user.password_salt)

    if password_hash != user.password_hash:
        return

    return user, token_service.register_new_token(user)

def logout(token: str) -> None:
    try:
        token_service.release_token(token)
    except Exception as e:
        raise Exception("Logout failed")