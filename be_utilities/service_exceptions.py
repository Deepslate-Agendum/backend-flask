class ServiceException(Exception):
    pass
class MissingException(ServiceException):
    pass
class AlreadyExistsException(ServiceException):
    pass
class InvalidParameterException(ServiceException):
    pass

