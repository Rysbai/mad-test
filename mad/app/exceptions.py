from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

UNEXPECTED_ERROR = "UnexpectedException"
NOT_FOUND = "ObjectDoesNotExist"
BAD_REQUEST = "BadRequest"
UNAUTHORIZED = "Unauthorized"
PERMISSION_DENIED = "PermissionDenied"

INVALID_TOKEN = "InvalidToken"
INCORRECT_LOGIN_OR_PASSWORD = "IncorrectLoginOrPassword"
USER_IS_NOT_ACTIVE = "UserIsNotActive"
USER_IS_NOT_DOCTOR = "UserIsNotDoctor"


def drf_exception_handler(exc, context):
    if isinstance(exc, MadBaseException):
        return Response({"code": exc.code, "message": exc.message}, status=exc.http_code)

    response = exception_handler(exc, context)
    if isinstance(exc, APIException):
        response.data = exc.get_full_details()
        return response

    return None


class MadBaseException(Exception):
    code = UNEXPECTED_ERROR
    message = "Unexpected error occurred while processing your request"
    http_code = 500

    def __init__(self, code: str = "", message: str = "", http_code: int = None):
        self.code = code or self.code
        self.message = message or self.message
        self.http_code = http_code or self.http_code


class MadBadRequest(MadBaseException):
    code = BAD_REQUEST
    message = "Bad request"
    http_code = 400


class MadNotFound(MadBaseException):
    code = NOT_FOUND
    message = "Object Does not exist"
    http_code = 404


class MadPermissionDenied(MadBaseException):
    code = PERMISSION_DENIED
    message = "Permission denied"
    http_code = 403


class MadUnauthorized(MadBaseException):
    code = UNAUTHORIZED
    message = "Unauthorized"
    http_code = 401
