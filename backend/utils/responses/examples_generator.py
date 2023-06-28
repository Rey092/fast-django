# -*- coding: utf-8 -*-
"""Examples generator module."""
from typing import List, Optional, Type

from starlette import status

from utils.responses.http.auth import (InsufficientRightsException,
                                       InvalidCredentialsException,
                                       UnauthorizedException)
from utils.responses.http.base import DefaultHTTPException
from utils.responses.http.success import SuccessResponse


class ExamplesGenerator:
    """Class to generate the examples for the OpenAPI docs."""

    auth_error = (
        UnauthorizedException,
        InvalidCredentialsException,
        InsufficientRightsException,
    )

    @staticmethod
    def generate_nested_schema_for_code(responses, error_code):
        """Generate the nested schema for the given error code."""
        responses[error_code] = {}
        responses[error_code]["content"] = {}
        responses[error_code]["content"]["application/json"] = {}

    @classmethod
    def generate_examples(
        cls,
        *args: Type[DefaultHTTPException],
        auth: bool = False,
        success_responses: Optional[List[SuccessResponse]] = None,
    ) -> dict:
        """Generate the error responses for the OpenAPI docs."""
        responses: dict = {}
        if auth:
            args += cls.auth_error

        error_codes = {error.status_code for error in args}

        for error_code in error_codes:
            examples = {}

            for error in args:
                instance = error()  # noqa
                if instance.status_code == error_code:
                    examples[instance.error] = instance.example()

            cls.generate_nested_schema_for_code(responses, error_code)
            responses[error_code]["content"]["application/json"]["examples"] = examples

        success_codes = {success.status_code for success in success_responses or []}

        for success_code in success_codes:
            examples = {}

            for success in success_responses:
                if success.status_code == success_code:
                    examples[success.message] = success.example()

            cls.generate_nested_schema_for_code(responses, success_code)
            responses[success_code]["content"]["application/json"]["examples"] = examples

        cls.change_422_validation_schema(responses)

        return responses

    @classmethod
    def change_422_validation_schema(cls, responses):
        """Change the 422 validation schema to match the one used in the API."""
        cls.generate_nested_schema_for_code(responses, status.HTTP_422_UNPROCESSABLE_ENTITY)
        example = {
            "validation_errors": {
                "summary": "Validation Error",
                "value": {
                    "status": 422,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "details": [
                            {
                                "location": "string",
                                "field": "string",
                                "message": "string",
                            }
                        ],
                    },
                },
            },
        }
        responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"]["examples"] = example


generate_examples = ExamplesGenerator.generate_examples
