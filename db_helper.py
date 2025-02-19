from mongoengine import connect
from db_classes import Field, ValueType

# function that opens a connection to the database
def connectToDatabase():
    host = "mongodb://localhost:27017/mongodb"
    connection = connect(host=host)
    if connection == None:
        raise Exception("Failed to connect to the database")
    return connection


# function that disconnects from the database
def disconnectFromDatabase(connection):
    connection.close()

# function that creates tag fields
def createTagField(name):
    tag_value_type = ValueType.objects(name = "Tag")

    tag_field = Field(name = name, min_values = 1, max_values = 1, default_allowed_value = None, value_type=tag_value_type)
    tag_field.save()

    return tag_field