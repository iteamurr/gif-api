import enum


class Error(enum.Enum):
    BAD_REQUEST = {
        "response": {
            "message": "Problems parsing JSON.",
            "code": 400,
        },
        "status": 400,
    }
    CONFLICT = {
        "response": {
            "message": "This content already exists.",
            "code": 409,
        },
        "status": 409,
    }
    NOT_FOUND = {
        "response": {
            "message": "The particular GIF you are requesting was not found.",
            "code": 404,
        },
        "status": 404,
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

    def __init__(self, vals) -> None:
        self.response = vals["response"]
        self.status = vals["status"]
