from rest_framework.response import Response
from rest_framework import status


def success_response(
    message,
    data=None,
    status_code=status.HTTP_200_OK,
    meta=None
):
    payload = {
        "success": True,
        "message": message,
        "data": data
    }

    if meta:
        payload["meta"] = meta

    return Response(payload, status=status_code)


def error_response(
    message,
    errors=None,
    status_code=status.HTTP_400_BAD_REQUEST
):
    payload = {
        "success": False,
        "message": message,
        "errors": errors
    }

    return Response(payload, status=status_code)