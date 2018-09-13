
class BaseValidatorException(Exception):

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(BaseValidatorException, self).__init__(message)


class WrongArguments(BaseValidatorException):
    pass


class ValidationException(BaseValidatorException):
    pass
