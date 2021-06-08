class WrongEmailFormatException(Exception):
    def __init__(self, message: str) -> None:
        super(WrongEmailFormatException, self).__init__(message)
        self.message = message

class UserAlreadyExistsException(Exception):
    def __init__(self, message: str) -> None:
        super(UserAlreadyExistsException, self).__init__(message)
        self.message = message

class UserDoesntExistsException(Exception):
    def __init__(self, message: str) -> None:
        super(UserDoesntExistsException, self).__init__(message)
        self.message = message

class WrongPasswordException(Exception):
    def __init__(self, message: str) -> None:
        super(WrongPasswordException, self).__init__(message)
        self.message = message
