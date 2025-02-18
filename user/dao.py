from typing import List, Optional
from db_classes import User


def get_by_id(id: str) -> Optional[User]:
    return User.with_id(id)

def get_by_username(name: str) -> Optional[User]:
    users = User.objects(username=name)
    return users[0] if len(users) > 0 else None

def get_all() -> List[User]:
    return list(User.objects)

def create(name, password_hash, password_salt) -> User:
    user = User(
        username=name,
        display_name=name, # TODO: we need a display name
        workspaces=[], # a user is not initially a member of any workspaces.
        tasks=[],
        owned_filtered_views=[],
        shared_filtered_views=[],
        password_hash=password_hash,
        password_salt=password_salt
    )
    user.save()
    return user

def update(id, name, password_hash) -> User:
    user = User.with_id(id)
    if id is None:
        raise ValueError(f"No user with id {id}!")

    user.name = name
    user.password_hash = password_hash
    return user

def delete(id: str) -> None:
    user = User.with_id(id)
    if id is None:
        raise ValueError(f"No user with id {id}!")

    user.delete()

def get_salt(id: str) -> str:
    user = User.with_id(id)
    if id is None:
        raise ValueError(f"No user with id {id}!")

    return user.salt
