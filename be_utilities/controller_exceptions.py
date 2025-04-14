class ControllerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class MissingArgumentException(ControllerException):
    pass
