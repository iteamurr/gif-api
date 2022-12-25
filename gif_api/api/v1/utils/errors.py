import enum


class Error(enum.Enum):
    NOT_FOUND = {
        "response": {
            "message": "The particular GIF you are requesting was not found.",
            "code": 404,
        },
        "status": 404,
    }
    CONFLICT = {
        "response": {
            "message": "This content already exists.",
            "code": 409,
        },
        "status": 409,
    }
    UNPROCESSABLE_ENTITY = {
        "response": {
            "message": (
                "Your request was formatted incorrectly "
                "or missing a required parameter(s)."
            ),
            "code": 422,
        },
        "status": 422,
    }
    SERVICE_UNAVAILABLE = {
        "response": {
            "message": "The server is temporarily unable to handle the request.",
            "code": 503,
        },
        "status": 503,
    }

    def __init__(self, vals) -> None:
        self.response = vals["response"]
        self.status = vals["status"]
