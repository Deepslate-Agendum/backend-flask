from mongoengine import Document, ListField, StringField, IntField, EmbeddedDocument, LazyReferenceField

class ValueType(Document):
    name = StringField(required=True)

    # static_fields # a value type is the type of 0+ static fields
    # fields # a value type is the type of 0+ fields
    allowed_values = ListField(LazyReferenceField('AllowedValue'))


class AllowedValue(Document):
    value = StringField(required=True)

    # dependency_type # an allowed value specifies the manner of 0+ dependency types
    # field_value # an allowed value provides the value for 0+ field values
    # field # an allowed value provides the default value for 0+ fields
    value_type = LazyReferenceField('ValueType', required=True) # an allowed value is of 1 type


class Field(EmbeddedDocument):
    name = StringField(required=True)
    min_values = IntField(required=True)
    max_values = IntField()

    # field_value # a field has 0+ values
    # static_task_types # a field belongs statically to 0+ task types
    # dynamic_task_types # a field belongs dynamically to 0+ task types
    default_allowed_value = LazyReferenceField('AllowedValue') # a field has 0/1 default values
    value_type = LazyReferenceField('ValueType', required=True) # a field has 1 value type


class FieldValue(Document):
    value = StringField() # (non-null iff allowed_value is null)

    task = LazyReferenceField('Task') # a field value belongs to 0/1 tasks (non-null iff task type is null)
    task_type = LazyReferenceField('TaskType') # a field value belongs to 0/1 task types (non-null iff task is null)
    field = LazyReferenceField('Field', required=True) # a field value belongs to 1 field
    allowed_value = LazyReferenceField('AllowedValue') # a field value is provided by 0/1 allowed values (non-null iff value is null)


class User(Document):
    username = StringField(required=True, unique=True)
    display_name = StringField(required=True)
    hash_password = StringField(required=True)
    hash_salt = StringField(required=True, unique=True) # !TODO: check with backend, do we enforce uniqueness?

    workspaces = ListField(LazyReferenceField('Workspace')) # a user belongs to 1+ workspaces !TODO: default workspace?
    tasks = ListField(LazyReferenceField('Task')) # a user is assigned 0+ tasks
    owned_filtered_views = ListField(LazyReferenceField('FilteredView')) # a user owns 0+ filtered views
    shared_filtered_views = ListField(LazyReferenceField('FilteredView')) # a user has shared with them 0+ filtered views
    

class Workspace(Document):
    name = StringField(required=True, unique=True)

    users = ListField(LazyReferenceField('User')) # a workspace has 1+ members
    task_types = ListField(LazyReferenceField('TaskType')) # a workspace has 1+ task types (default when created)
    tasks = ListField(LazyReferenceField('Task')) # a workspace has 0+ tasks
    # filtered_views # a workspace is the domain of 0+ filtered views


class TaskType(Document):
    name = StringField(required=True)

    static_fields = ListField(LazyReferenceField('Field')) # a task type has 0+ static fields 
    nonstatic_fields = ListField(LazyReferenceField('Field')) # a task type has 0+ non-static fields
    static_field_values = ListField(LazyReferenceField('FieldValue')) # a task type has 0+ static field values
    # tasks # a task type is the type of 0+ tasks
    workspaces = ListField(LazyReferenceField('Workspace')) # a task type belongs to 0+ workspaces
    dependency_types = ListField(LazyReferenceField('DependencyType')) # a task type groups its dependencies through 0+ dependency types



class Task(Document):
    # no intrinsic attributes

    nonstatic_field_values = ListField(LazyReferenceField('FieldValue')) # a task has 0+ non-static field values
    dependencies = ListField(LazyReferenceField('Dependency')) # a task depends on (0+) tasks via 0+ dependencies
    # workspaces = ListField(LazyReferenceField('Workspace')) # a task belongs to 1+ workspaces # TODO: are we doing same task in multiple workspaces?
    task_type = LazyReferenceField('TaskType', required=True) # a task is of 1 task type


class DependencyType(EmbeddedDocument):
    name = StringField(required=True)
    minTasks = IntField(required=True)
    maxTasks = IntField()

    # task_type # a dependency type groups the dependencies of 1 task type
    # dependency # a dependency type groups 0+ dependencies
    allowed_values = LazyReferenceField('AllowedValue', required=True) # a dependency type's manner (subtask / blocker) is specified by 1 allowed value


class Dependency(Document):
    # no intrinsic attributes

    depended_on_task = LazyReferenceField('Task', required=True) # a dependency expresses a task's dependence on 1 task
    dependent_task = LazyReferenceField('Task', required=True) # a dependency expresses the dependence of 1 task
    dependency_type = LazyReferenceField('DependencyType', required=True) # a dependency is of 1 dependency type


class FilteredView(Document):
    name = StringField(required=True)
    query = StringField(required=True)

    owner_user = LazyReferenceField('User') # a filtered view is owned by 1 user
    shared_with_users = ListField(LazyReferenceField('User')) # a filtered view is shared with 0+ (non-owning) users
    workspaces = ListField(LazyReferenceField('Workspace', required=True)) # a filtered view belongs to 1+ workspaces
