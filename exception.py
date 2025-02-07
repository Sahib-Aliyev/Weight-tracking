from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "server error"

    def __init__(self):
        super().__init__(status_code=self.STATUS_CODE,
                         detail=self.DETAIL)


class UserNotFoundException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "User is not found"


class InvalidPassword(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Invalid password"


class UserAlreadyExist(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "User already exist"


class WeightNotFoundException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Weight is not found"
