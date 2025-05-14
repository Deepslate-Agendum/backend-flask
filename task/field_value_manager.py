from typing import Union
from db_python_util.db_classes import FieldValue, AllowedValue, Task

from mongoengine import Document


# TODO: this will have to be reworked for cardinality requirements (ie don't save values immediately)
class FieldValueManager:
    def __init__(self, task: Task, field, values):
        self.task = task
        self.field = field
        self.values = values

    def get_name(self) -> str:
        name = self.field.name
        return name

    def get_count(self) -> int:
        count = len(self.values)
        return count

    # TODO: deserialization based on type?
    def get_value(self, index: int) -> Union[str, AllowedValue]:
        field_value = self.values[index]
        value = field_value.value or field_value.allowed_value.fetch()
        return value

    def set_value(self, index: int, value: str) -> None:
        field_value_reference = self.values[index]
        field_value = field_value_reference.fetch()
        field_value.update(value=value)
        field_value.save()

    # TODO: validation based on whether field type is an enum?
    def _add_field_value(self, field_value: FieldValue):
        field_value.save()
        self.values.append(field_value)
        self.task.nonstatic_field_values.append(field_value)
        self.task.save()

    def add_value(self, value: str) -> None:
        field_value = FieldValue(
            value=value,
            field=self.field,
        )
        self._add_field_value(field_value)

    def add_allowed_value(self, value: AllowedValue) -> None:
        field_value = FieldValue(
            allowed_value=value,
            field=self.field,
        )
        self._add_field_value(field_value)

    def pop_value(self, index: int) -> None:
        field_value_reference = self.values.pop(index)
        self.task.nonstatic_field_values.remove(field_value_reference)
        self.task.save()

        field_value = field_value_reference.fetch()
        field_value.delete()
