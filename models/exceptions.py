class DataException(Exception):
    def __init__(self, message):
        self.message = message


class GetRemoteDataException(DataException):
    def __init__(self, message):
        super().__init__(message)