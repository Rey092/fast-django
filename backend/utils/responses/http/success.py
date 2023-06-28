# -*- coding: utf-8 -*-
"""Success HTTP response."""
from enum import Enum
from typing import Optional

from starlette.responses import JSONResponse


class SuccessStatus(str, Enum):
    """Success status."""

    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    INFO = "INFO"
    DANGER = "DANGER"


class SuccessResponse(JSONResponse):
    """Default class for all HTTP exceptions."""

    def __init__(
        self,
        message: Optional[str] = None,
        status: SuccessStatus = SuccessStatus.SUCCESS,
        status_code: int = 200,
        *args,
        **kwargs,
    ):
        """Initialize the exception."""
        self.message = message
        self.status = status
        self.status_code = status_code
        super(SuccessResponse, self).__init__(
            content=self.example()["value"],
            status_code=self.status_code,
            *args,
            **kwargs,
        )

    def example(self) -> dict:
        """Return an example of the error response. This is used in the OpenAPI docs."""
        example = {
            "summary": self.message,
            "value": {
                "status": self.status,
                "message": self.message,
            },
        }
        return example
