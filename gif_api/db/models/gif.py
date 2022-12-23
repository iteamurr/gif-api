import enum

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql as psql

from gif_api import db


class GifRating(str, enum.Enum):
    Y = "y"
    G = "g"
    PG = "pg"
    PG13 = "pg-13"
    R = "r"


class Gif(db.Base):
    __tablename__ = "gif"

    gif_id = sa.Column(
        psql.UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        server_default=sa.sql.func.gen_random_uuid(),
        doc="This GIF's unique ID.",
    )
    title = sa.Column(
        sa.String(length=127),
        nullable=False,
        doc="The title for this GIF.",
    )
    url = sa.Column(
        sa.String(length=255),
        nullable=False,
        unique=True,
        doc="The unique URL for this GIF.",
    )
    rating = sa.Column(
        sa.Enum(GifRating),
        nullable=False,
        server_default="G",
        doc="The MPAA-style rating for this content.",
    )
    create_datetime = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.sql.func.now(),
        doc="The date this GIF was added to the database.",
    )
    update_datetime = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        onupdate=sa.sql.func.now(),
        server_default=sa.sql.func.now(),
        doc="The date on which this GIF was last updated.",
    )

    trendings = orm.relationship("Trending", back_populates="trending_gif")

    def __repr__(self) -> str:
        return f"<Gif '{self.gif_id}'>"
