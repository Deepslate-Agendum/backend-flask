from db_classes import TaskType, Field, ValueType, User
from db_helper import connectToDatabase, disconnectFromDatabase



# NOTE: currently not in use
# # function that creates the admin user and saves it to the database 
# def createAdminUser():
#     connection = connectToDatabase()

#     admin_user = User(username="admin", display_name="admin", hash_password="password", hash_salt="password", workspaces=[], tasks=[], owned_filtered_views=[], shared_filtered_views=[])
#     admin_user.save()

#     disconnectFromDatabase(connection)


# function that creates the default task type and saves it to the database
def createDefaultTaskType():

    # create a Tag Value Type
    tag_value_type = ValueType(name="Tag", allowed_values=[])
    tag_value_type.save()

    # create default ValueTypes: string and user
    string_value_type = ValueType(name="String", allowed_values=[])
    user_value_type = ValueType(name="User", allowed_values=[])
    string_value_type.save()
    user_value_type.save()

    # create system fields: Name, Assignee, Description, Due Date
    name_system_field = Field(name="Name", min_values=1, max_values=1, default_allowed_value = None, value_type=string_value_type)
    assignee_system_field = Field(name="Assignee", min_values=0, max_values=1, default_allowed_value = None, value_type = user_value_type)
    description_system_field = Field(name="Description", min_values=1, max_values=1, default_allowed_value = None, value_type=string_value_type)
    due_date_system_field = Field(name="Due Date", min_values=0, max_values=1, default_allowed_value = None, value_type=string_value_type)
    name_system_field.save()
    assignee_system_field.save()
    description_system_field.save()
    due_date_system_field.save()

    # create default task type
    default_task_type = TaskType(name="Default", static_fields = [], nonstatic_fields = [name_system_field, assignee_system_field, description_system_field, due_date_system_field], static_field_values=[], workspaces = [], dependency_types = [])
    default_task_type.save()



def main():
    connection = connectToDatabase()
    
    createDefaultTaskType()

    disconnectFromDatabase(connection)



if __name__ == "__main__":
    main()
