import secrets
from datetime import datetime, timedelta

USER_TOKEN_LENGTH = 64
TOKEN_EXPIRY_DURATION = timedelta(hours=1)

# This is hacky, but it seems to be the simplest and memory isn't
# a concern for us.
user_to_token_map = {}
token_to_user_data_map = {}

class UserData:
    def __init__(self, user_id, last_used_timestamp: datetime):
        self.user_id = user_id
        self.last_used_timestamp = last_used_timestamp


def generate_token() -> bytes:
    """Do not use, internal function for user token generation"""
    return secrets.token_bytes(USER_TOKEN_LENGTH)

def register_new_token(user_id: str) -> bytes:
    """Register a token to a user who has been authenticated"""
    existing_token = user_to_token_map.get(user_id)
    if existing_token is not None:
        refresh_token(existing_token)
        return existing_token

    token = generate_token()
    while token_to_user_data_map.get(token) is not None:
        token = generate_token()

    user_to_token_map[user_id] = token
    token_to_user_data_map[token] = UserData(user_id, datetime.now())

    return token

def authenticate_token(token: bytes) -> str:
    """Get the user that a token is assigned to, after validating that the token is still valid"""
    refresh_token(token)

    return token_to_user_data_map.get(token).user_id

def refresh_token(token: bytes) -> None:
    """Refresh a token, pushing expiry time to 15 minutes from now"""
    if token_to_user_data_map.get(token) is None:
        raise Exception("Token does not exist")

    if token_to_user_data_map.get(token).last_used_timestamp + TOKEN_EXPIRY_DURATION < datetime.now():
        release_token(token)
        raise Exception("Token has expired and has now been deleted")

    token_to_user_data_map.get(token).last_activity_timestamp = datetime.now()

def release_token(token: bytes) -> None:
    """Release a token, effectively logging out a user"""
    if token_to_user_data_map.get(token) is None:
        raise Exception("Token does not exist")

    user = token_to_user_data_map.pop(token)
    user_to_token_map.pop(user)
