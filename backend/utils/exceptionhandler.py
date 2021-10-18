from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handle_standardized_exception_error,
        'Http404': _handle_standardized_exception_error,
        'PermissionDenied': _handle_standardized_exception_error,
        'NotAuthenticated': _handle_standardized_exception_error,
        'ParseError': _handle_standardized_exception_error,
        'AuthenticationFailed': _handle_standardized_exception_error,
        'NotFound': _handle_standardized_exception_error,
        'MethodNotAllowed': _handle_standardized_exception_error,
        'NotAcceptable': _handle_standardized_exception_error,
        'UnsupportedMediaType': _handle_standardized_exception_error,
        'Throttled': _handle_standardized_exception_error
    }

    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_standardized_exception_error(exc, context, response):
    response.data = {
        "error": {
            "message": str(exc),
            "type": exc.__class__.__name__,
            "code": exc.status_code,
        }
    }
    return response
