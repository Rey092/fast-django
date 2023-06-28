# -*- coding: utf-8 -*-
"""Base service for managing some model."""
from abc import ABC
from typing import List, Optional, Type, final

from django.db.models import Model

from utils.repositories import BaseRepository


class BaseService(ABC):
    """
    Abstract base service for managing some model.
    """

    model: Type[Model]
    repository: BaseRepository

    @final
    async def get_all(self, *args, **kwargs):
        """Get all items."""
        return await self.repository.get_all(*args, **kwargs)

    @final
    async def get_all_and_count(self, *args, **kwargs):
        """Get all items and count."""
        return await self.repository.get_all_and_count(*args, **kwargs)

    @final
    async def get_one(
        self,
        raise_not_found: bool = True,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        **kwargs,
    ):
        """Get one item."""
        return await self.repository.get_one(
            raise_not_found=raise_not_found,
            select_related=select_related,
            prefetch_related=prefetch_related,
            **kwargs,
        )

    @final
    async def get_one_by_id(
        self,
        item_id: int,
        raise_not_found: bool = True,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        **kwargs,
    ):
        """Get one item by id."""
        item = await self.repository.get_one_by_id(
            item_id=item_id,
            raise_not_found=raise_not_found,
            select_related=select_related,
            prefetch_related=prefetch_related,
            **kwargs,
        )
        return item

    @final
    async def get_one_by_slug(
        self,
        slug: str,
        raise_not_found: bool = True,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        **kwargs,
    ):
        """Get one item by slug."""
        return await self.repository.get_one_by_slug(
            slug,
            raise_not_found=raise_not_found,
            select_related=select_related,
            prefetch_related=prefetch_related,
            **kwargs,
        )

    @final
    async def get_or_create_one(self, *args, **kwargs):
        """Get or create one item."""
        return await self.repository.get_or_create_one(*args, **kwargs)

    @final
    async def create_one(self, *args, **kwargs):
        """Create one item."""
        return await self.repository.acreate_one(*args, **kwargs)

    @final
    async def save_one(self, *args, **kwargs):
        """Update one item by id."""
        return await self.repository.save_one(*args, **kwargs)

    @final
    def save_one_sync(self, *args, **kwargs):
        """Update one item by id."""
        return self.repository.save_one_sync(*args, **kwargs)

    @final
    async def delete_one(self, raise_not_found: bool = True, **kwargs):
        """Delete one item by id."""
        return await self.repository.delete_one(raise_not_found, **kwargs)

    @final
    async def delete_one_by_id(self, item_id: int, raise_not_found: bool = True, **kwargs):
        """Delete one item by id."""
        return await self.repository.delete_one_by_id(item_id, raise_not_found, **kwargs)
