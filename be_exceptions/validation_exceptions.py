class ValidationException(Exception):
    pass
class MissingException(ValidationException):
    pass
class AlreadyExistsException(ValidationException):
    pass
class InvalidParameterException(ValidationException):
    pass

