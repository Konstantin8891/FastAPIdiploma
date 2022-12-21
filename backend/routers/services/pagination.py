from __future__ import annotations

from typing import Generic, Sequence, TypeVar, Any, Type

from abc import ABC
from functools import update_wrapper
from fastapi import Query, Request
from pydantic import BaseModel, conint, create_model
from sqlalchemy.orm import Session
from types import new_class

from fastapi_pagination.bases import AbstractParams, RawParams, TAbstractPage, _create_params, AbstractPage
from fastapi_pagination.types import GreaterEqualZero

import sys
sys.path.append('..')

from routers.auth import get_db

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    limit: int = Query(50, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.limit,
            offset=self.limit * (self.page - 1),
        )


class BasePage(AbstractPage[T], Generic[T], ABC):
    results: Sequence[T]
    count: GreaterEqualZero


class Page(BasePage[T], Generic[T]):
    page: conint(ge=1)  # type: ignore
    limit: conint(ge=1)  # type: ignore
    previous: str

    def __init__(self, page: conint, limit: conint, request: Request):
        self.page = page
        self.limit = limit
        if page == 1:
            self.previous = None
        else:
            self.previous = f'http://{request.url}?page={str(page - 1)}'

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        # previous: str,
        params: AbstractParams,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(
            count=total,
            results=items,
            page=params.page,
            limit=params.limit,
            previous=cls.previous
        )

    @classmethod
    def with_custom_options(cls: Type[TAbstractPage], **kwargs: Any) -> Type[TAbstractPage]:
        params_cls = cls.__params_type__

        custom_params: Any = create_model(  # noqa
            params_cls.__name__,
            __base__=params_cls,
            **_create_params(params_cls, kwargs),
        )

        bases: Tuple[Type, ...]
        if cls.__concrete__:
            bases = (cls,)
        else:
            params = tuple(cls.__parameters__)
            bases = (cls[params], Generic[params])  # type: ignore[assignment, index]

        new_cls = new_class("CustomPage", bases, exec_body=lambda ns: setitem(ns, "__params_type__", custom_params))
        new_cls = update_wrapper(new_cls, cls, updated=())

        return new_cls  # noqa


__all__ = [
    "Params",
    "Page",
]