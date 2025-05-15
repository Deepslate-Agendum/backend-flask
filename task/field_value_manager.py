from typing import List, Optional, Union
from db_python_util.db_classes import FieldValue, AllowedValue, Task

from mongoengine import Document

from db_python_util.db_exceptions.db_integrity_exception import DBIntegrityException


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
        value = field_value.value if field_value.value is not None else field_value.allowed_value.fetch()
        return value

    def get_values(self) -> List[Union[str, AllowedValue]]:
        values = [self.get_value(i) for i in range(self.get_count())]
        return values

    def set_value(self, index: int, value: Union[str, AllowedValue]) -> None:
        if isinstance(value, str):
            self._set_field_value(index, value, None)
        else:
            self._set_field_value(index, None, value)

    def add_value(self, value: Union[str, AllowedValue]) -> None:
        if isinstance(value, str):
            field_value = FieldValue(
                value=value,
                field=self.field,
            )
        else:
            field_value = FieldValue(
                allowed_value=value,
                field=self.field,
            )

        self._add_field_value(field_value)

    def _add_field_value(self, field_value: FieldValue):
        field_value.save()
        self.values.append(field_value)
        self.task.nonstatic_field_values.append(field_value)
        self.task.save()

    def _set_field_value(self, index: int, value: Optional[str], allowed_value: Optional[AllowedValue]):
        if (value is None) == (allowed_value is None):
            raise DBIntegrityException(FieldValue, "Exactly one of `value` or `allowed_value` must be non-null.")

        field_value_reference = self.values[index]
        field_value = field_value_reference.fetch()
        field_value.update(
            value=value,
            allowed_value=allowed_value,
        )
        field_value.save()

    def pop_value(self, index: int) -> None:
        field_value_reference = self.values.pop(index)
        self.task.nonstatic_field_values.remove(field_value_reference)
        self.task.save()

        field_value = field_value_reference.fetch()
        field_value.delete()
