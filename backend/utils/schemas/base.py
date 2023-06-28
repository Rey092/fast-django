# -*- coding: utf-8 -*-
"""Base schema for all API schemas."""
from typing import Any, List

from humps.main import camelize
from ninja import Schema


class DjangoSchema(Schema):
    """Base schema for all API schemas."""

    class Config:
        """Pydantic config."""

        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
        underscore_attrs_are_private = True

    def compute(self):
        """Compute all fields."""
        pass

    def adjust(self, **kwargs):
        """Adjust fields."""
        if isinstance(super(), DjangoSchema):
            super().adjust(**kwargs)  # noqa

        # call adjust method for all attributes that have it
        for attr in self.__dict__.values():
            if isinstance(attr, DjangoSchema):
                attr.adjust(**kwargs)

        return self

    @classmethod
    def from_orm(cls, obj: Any):
        """Create schema from ORM model."""
        obj = super().from_orm(obj)
        obj.compute()  # noqa
        return obj

    @classmethod
    def from_orm_adjusted(cls, obj: Any, **kwargs):
        """Create schema from ORM model."""
        obj = super().from_orm(obj)
        obj.adjust(**kwargs)  # noqa
        return obj

    @classmethod
    def from_list(cls, objs: List[Any]):
        """Create schema from ORM model."""
        objs = [cls.from_orm(obj) for obj in objs]
        return objs

    @classmethod
    def from_list_adjusted(cls, objs: List[Any], **kwargs):
        """Adjust list of objects."""
        objs = cls.from_list(objs)
        [obj.adjust(**kwargs) for obj in objs]
        return objs
