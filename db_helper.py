from functools import wraps

from mongoengine import connect, disconnect
from db_classes import Field, ValueType


# function that opens a connection to the database
def connectToDatabase():
    host = "mongodb://localhost:27017/mongodb"
    connection = connect(host=host)
    if connection is None:
        raise ConnectionError("Failed to connect to the database")
    return connection


class ConnectionManager:
    def __init__(self):
        self._connection = None

    def get_connection(self):
        if self._connection is None:
            self._connection = connectToDatabase()

        return self._connection

    def requires_connection(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            nonlocal self
            self.get_connection()
            return f(*args, **kwargs)
        return wrapped

ConnectionManager = ConnectionManager()


# NOTE: this function is currently being worked on as it is used in AGENDUM-36 which is not complete.
# # function that creates tag fields
# def createTagField(name):
#     tag_value_type = ValueType.objects(name = "Tag")

#     tag_field = Field(name = name, min_values = 1, max_values = 1, default_allowed_value = None, value_type=tag_value_type)
#     tag_field.save()

#     return tag_field
