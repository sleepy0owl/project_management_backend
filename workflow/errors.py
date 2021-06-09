class MaxBoardLimitReachedException(Exception):
    def __init__(self, message: str) -> None:
        super(MaxBoardLimitReachedException, self).__init__(message)
        self.message = message
