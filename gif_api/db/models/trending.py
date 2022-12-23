import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql as psql

from gif_api import db


class Trending(db.Base):
    __tablename__ = "trending"

    trending_id = sa.Column(
        psql.UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        server_default=sa.sql.func.gen_random_uuid(),
        doc="Trending's unique ID.",
    )
    gif_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey("gif.gif_id", ondelete="CASCADE"),
        nullable=False,
        doc="The GIF that took the current place in the trends.",
    )
    trending_date = sa.Column(
        sa.Date,
        nullable=False,
        server_default=sa.sql.func.now(),
        doc="The date on which the GIF was trending.",
    )

    trending_gif = orm.relationship("Gif", back_populates="trendings")

    def __repr__(self) -> str:
        return f"<Trending '{self.trending_id}'>"
