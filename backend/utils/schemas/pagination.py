# -*- coding: utf-8 -*-
"""FastAPI pagination schemas."""
from math import ceil
from typing import List

from fastapi import Query
from fastapi_pagination import LimitOffsetParams, Params
from fastapi_pagination.bases import AbstractParams
from pydantic import BaseModel


class LimitOffsetPaginator(BaseModel):
    """Base paginator."""

    entries: List
    count: int
    total_count: int
    limit: int = Query(..., ge=1, description="Limit of transactions per page")
    offset: int = Query(..., ge=0, description="Limit of transactions per page")

    @classmethod
    def create(
        cls,
        entries: List,
        params: LimitOffsetParams,
        total_count: int,
    ) -> "LimitOffsetPaginator":
        """Create paginator instance."""
        return cls(
            entries=entries,
            count=len(entries),
            total_count=total_count,
            limit=params.limit,
            offset=params.offset,
        )


class PageNumberedPaginator(BaseModel):
    """Base paginator."""

    entries: List
    count: int
    total_count: int
    size: int = Query(..., ge=1, description="Limit of transactions per page")
    page: int = Query(..., ge=1, description="Page number")
    pages: int = Query(..., ge=1, description="Total pages")

    @classmethod
    def create(
        cls,
        entries: List,
        params: AbstractParams,
        total_count: int,
    ) -> "PageNumberedPaginator":
        """Create paginator instance."""
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        pages = ceil(total_count / params.size) if total_count else 1

        return cls(
            entries=entries,
            count=len(entries),
            total_count=total_count,
            page=params.page,
            size=params.size,
            pages=pages,
        )
