from collections import defaultdict
from typing import Union

from db_python_util.db_classes import AllowedValue, Field, Task
from db_python_util.db_exceptions.db_integrity_exception import DBIntegrityException
from task.field_value_manager import FieldValueManager


class FieldManager:
    def __init__(self, task: Task):
        self.task = task
        self.name_map = self._map_fields()

    # TODO: swap out names for ids because of uniqueness issue
    def _map_fields(self):
        field_values_map = defaultdict(list)
        name_field_map = defaultdict(list)

        for field in self.task.task_type.nonstatic_fields:
            name_field_map[field.name] = field

        for field_value in self.task.nonstatic_field_values:
            name_field_map[field_value.field.name] = field_value.field
            field_values_map[field_value.field].append(field_value)

        name_map = {
            name: FieldValueManager(self.task, field, field_values_map[field])
            for name, field in name_field_map.items()
        }

        return name_map

    def fetch_field(self, name):
        # TODO: fields are not guaranteed to be unique by name (probably should include the type)
        fields = Field.objects(name=name)
        if len(fields) != 1:
            raise DBIntegrityException(Field, f"Field '{name}' could not be resolved in the database!")

        field = fields[0]
        return field

    def get_field_manager(self, name):
        field_manager = self.name_map.get(name)
        if field_manager is None:
            field = self.fetch_field(name)
            field_manager = self.name_map[name] = FieldValueManager(self.task, field, [])

        return field_manager

    def get_field_value_count(self, name) -> int:
        field_manager = self.get_field_manager(name)
        count = field_manager.get_count()
        return count

    def get_field_value(self, name, index: int) -> str:
        field_manager = self.get_field_manager(name)
        value = field_manager.get_value(index)
        return value

    def set_field_value(self, name, index: int, value: str) -> None:
        field_manager = self.get_field_manager(name)
        field_manager.set_value(index, value)

    def add_field_value(self, name, value: Union[str, AllowedValue]) -> None:
        field_manager = self.get_field_manager(name)

        if isinstance(value, str):
            field_manager.add_value(value)
        else:
            field_manager.add_allowed_value(value)

    def pop_field_value(self, name, index: int) -> None:
        field_manager = self.get_field_manager(name)
        field_manager.pop_value(index)

    def to_dictionary(self):
        dictionary = {
            name: [field_manager.get_value(i) for i in range(field_manager.get_count())]
            for name, field_manager in self.name_map.items()
        }
        return dictionary
