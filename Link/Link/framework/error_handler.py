from flask import json
from flask import Response


def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def handle_all_exception(e):
    code = getattr(e, "code", 500)
    response = Response(status=code)

    response.data = json.dumps({
        "code": code,
        "name": "Server Error",
        "description": str(e) or "Apologies for the Inconvenience caused"
    })

    response.content_type = "application/json"
    return response
