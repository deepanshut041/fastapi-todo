from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
import datetime
from sqlalchemy import DateTime


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }
