from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        custom_response_data = {
            "error": "Authentication Failed",
            "details": "Please login again or refresh your token."
        }
        response.data = custom_response_data

    return response