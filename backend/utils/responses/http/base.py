# -*- coding: utf-8 -*-
"""Base HTTP exceptions."""
import abc
from abc import abstractproperty
from typing import Optional

from fastapi import HTTPException  # noqa


class ClassABC(type):
    """Metaclass for abstract classes."""

    def __init__(cls, name, bases, attrs):
        """Initialize the class."""
        abstracts = set()

        for base in bases:
            abstracts.update(getattr(base, "__abstractclassmethods__", set()))

        for abstract in abstracts:
            annotation_type = bases[0].__annotations__.get(abstract)
            if annotation_type:
                if not isinstance(getattr(cls, abstract), annotation_type):
                    raise TypeError("Wrong type of {}".format(abstract))

                if getattr(getattr(cls, abstract), "__isabstractmethod__", False):
                    raise TypeError("Your class doesn't define {}".format(abstract))

        for attr in attrs:
            if getattr(attrs[attr], "__isabstractmethod__", False):
                abstracts.add(attr)

        cls.__abstractclassmethods__ = abstracts

        super().__init__(name, bases, attrs)


class BaseHTTPException(HTTPException, metaclass=ClassABC):
    """Simple base class for all HTTP exceptions."""

    status_code: int = 400

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__(status_code=self.status_code)

    @abc.abstractmethod
    def example(self) -> dict:
        """Return an example of the error response. This is used in the OpenAPI docs."""
        pass


class DefaultHTTPException(BaseHTTPException):
    """Default class for all HTTP exceptions."""

    error: str = abstractproperty()
    message: str = abstractproperty()

    def __init__(self, message: Optional[str] = None):
        """Initialize the exception."""
        self.message = message if message else self.message
        super(DefaultHTTPException, self).__init__()

    def example(self) -> dict:
        """Return an example of the error response. This is used in the OpenAPI docs."""
        example = {
            "summary": self.error,
            "value": {
                "status": self.status_code,
                "error": {
                    "code": self.error,
                    "message": self.message,
                },
            },
        }
        return example
