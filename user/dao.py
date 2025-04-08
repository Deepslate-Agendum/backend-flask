from typing import List, Optional

from mongoengine.errors import (
    ValidationError,
    NotUniqueError,
)

from dao_shared import get_document_by_id
from db_python_util.db_classes import User
from db_python_util.db_helper import ConnectionManager
from db_python_util.db_exceptions import (
    EntityNotFoundException,
    UsernameTakenException,
)


@ConnectionManager.requires_connection
def get_by_id(id: str) -> User:
    try:
        user = get_document_by_id(User, id)
    except ValidationError: # An ObjectId "must be a 12-byte input or a 24-character hex string", but front-end shouldn't need to care about that
        user = None

    if user is None:
        raise EntityNotFoundException(
            User,
            f"No user with id {id}"
        )

    return user

@ConnectionManager.requires_connection
def get_by_username(name: str) -> Optional[User]:
    return User.objects(username=name).first()

@ConnectionManager.requires_connection
def get_all() -> List[User]:
    return list(User.objects)

@ConnectionManager.requires_connection
def create(name: str, password_hash: str, password_salt: str) -> str:
    user = User(
        username=name,
        display_name=name, # TODO: we need a display name
        workspaces=[], # Note: By design, a user is not initially a member of any workspaces.
        tasks=[],
        owned_filtered_views=[],
        shared_filtered_views=[],
        password_hash=password_hash,
        password_salt=password_salt
    )

    try:
        user.save()
    except NotUniqueError:
        raise UsernameTakenException(name)

    return user.id.binary.hex()

@ConnectionManager.requires_connection
def update(id: str, name: str, password_hash: str):
    user = get_by_id(id)

    user_with_name = get_by_username(name)
    if (user_with_name is not None) and (user_with_name.id != user.id):
        raise UsernameTakenException(name)

    user.update(
        username=name,
        display_name=name, # TODO: we need a display name
        password_hash=password_hash,
    )

@ConnectionManager.requires_connection
def delete(id: str):
    user = get_by_id(id)
    user.delete()
