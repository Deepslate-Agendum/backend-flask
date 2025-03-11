from typing import List, Optional

import sys

from db_python_util.db_classes import User
from db_python_util.db_helper import ConnectionManager


@ConnectionManager.requires_connection
def get_by_id(id: str) -> Optional[User]:
    return User.objects.with_id(id)

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
    user.save()
    return user.id.binary.hex()

@ConnectionManager.requires_connection
def update(id: str, name: str, password_hash: str) -> bool:
    user = User.objects.with_id(id)
    if user is None:
        sys.stderr.write(f"No user with id {id}!\n")
        return False

    user_with_name = get_by_username(name)
    if (user_with_name is not None) and (user_with_name.id != user.id):
        sys.stderr.write(f"The username '{name}' is already taken!\n")
        return False

    user.update(
        username=name,
        display_name=name, # TODO: we need a display name
        password_hash=password_hash,
    )
    return True

@ConnectionManager.requires_connection
def delete(id: str) -> bool:
    user = User.objects.with_id(id)
    if id is None:
        sys.stderr.write(f"No user with id {id}!\n")
        return False

    user.delete()
    return True
