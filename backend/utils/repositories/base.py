# -*- coding: utf-8 -*-
"""Base repository module for defining abstract repository interfaces."""
from abc import ABC
from typing import Any, List, Optional, Tuple, Type, final

from asgiref.sync import sync_to_async
from django.db.models import Model

from utils.responses.http.api import NotFoundException


class BaseRepository(ABC):
    """
    An abstract interface for a repository.
    """

    model: Type[Model]

    @final
    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        **kwargs,
    ) -> List[Any]:
        """
        List all items.
        """
        qs = self.model.objects.filter(**kwargs)

        if select_related:
            qs = qs.select_related(*select_related)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)
        if order_by:
            qs = qs.order_by(*order_by)
        if limit and not offset:
            qs = qs[:limit]
        elif limit and offset:
            qs = qs[offset : offset + limit]

        return [item async for item in qs]

    @final
    async def get_all_and_count(self, *args, **kwargs) -> Tuple[list, int]:
        """
        List all items and count.
        """
        qs = self.model.objects.all()
        items = [item async for item in qs]
        total_count = await qs.acount()
        return items, total_count

    @final
    async def get_one(
        self,
        raise_not_found: bool = True,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        **kwargs,
    ):
        """
        Get an existing item.
        """
        select_related = select_related or []
        prefetch_related = prefetch_related or []

        # create a query set
        qs = self.model.objects.select_related(*select_related).prefetch_related(*prefetch_related).aget(**kwargs)
        # get the object
        try:
            obj = await qs
        except self.model.DoesNotExist:
            obj = None

        # raise not found exception
        if raise_not_found and not obj:
            raise NotFoundException()

        return obj

    @final
    async def get_one_by_id(
        self,
        item_id: int,
        raise_not_found: bool = True,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        **kwargs,
    ):
        """
        Get an existing item by ID.
        """
        obj = await self.get_one(
            id=item_id,
            raise_not_found=raise_not_found,
            select_related=select_related,
            prefetch_related=prefetch_related,
            **kwargs,
        )

        return obj

    @final
    async def get_one_by_slug(
        self,
        slug: str,
        raise_not_found: bool = True,
        select_related: Optional[List[str]] = None,
        prefetch_related: Optional[List[str]] = None,
        **kwargs,
    ):
        """
        Get an existing item by slug.
        """
        obj = await self.get_one(
            slug=slug,
            raise_not_found=raise_not_found,
            select_related=select_related,
            prefetch_related=prefetch_related,
            **kwargs,
        )

        return obj

    @final
    async def get_or_create_one(self, *args, **kwargs) -> Tuple[Any, bool]:
        """
        Get or create an existing item.
        """
        return await self.model.objects.aget_or_create(*args, **kwargs)

    @final
    async def update_or_create_one(self, *args, **kwargs) -> Tuple[Any, bool]:
        """
        Update or create an existing item.
        """
        return await self.model.objects.aupdate_or_create(*args, **kwargs)

    @final
    def create_one(self, **kwargs):
        """
        Create a new item.
        """
        return self.model.objects.create(**kwargs)

    @final
    async def acreate_one(self, *args, **kwargs):
        """
        Create a new item.
        """
        return await sync_to_async(self.create_one)(**kwargs)

    @sync_to_async
    @final
    def save_one(self, obj: Model):
        """
        Save an existing item.
        """
        obj.save()
        return obj

    @staticmethod
    @final
    def save_one_sync(obj: Model):
        """
        Save an existing item.
        """
        obj.save()
        return obj.refresh_from_db()

    @final
    async def delete_one(self, raise_not_found: bool = True, **kwargs) -> [bool, int]:
        """
        Delete an existing item.
        """
        item = await self.get_one(raise_not_found=raise_not_found, **kwargs)

        if item:
            return await self.model.objects.filter(id=item.id).adelete()

    @final
    async def delete_one_by_id(self, item_id: int, raise_not_found: bool = True, **kwargs) -> None:
        """
        Delete an existing item by ID.
        """
        await self.delete_one(id=item_id, raise_not_found=raise_not_found, **kwargs)

    @final
    async def delete_one_by_slug(self, slug: str, raise_not_found: bool = True, **kwargs) -> None:
        """
        Delete an existing item by slug.
        """
        await self.delete_one(slug=slug, raise_not_found=raise_not_found, **kwargs)

    @final
    async def bulk_create(self, objs: List[Model]) -> List[Model]:
        """
        Bulk create items.
        """
        return await self.model.objects.abulk_create(objs)

    @final
    def delete_many_sync(self, **kwargs) -> None:
        """Delete many items."""
        self.model.objects.filter(**kwargs).delete()

    @final
    async def delete_many(self, **kwargs) -> None:
        """Delete many items."""
        await sync_to_async(self.delete_many_sync)(**kwargs)
