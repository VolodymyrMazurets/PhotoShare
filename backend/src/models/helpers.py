from sqlalchemy import Column, Integer, ForeignKey, Table
from src.models.base_model import Base

post_m2m_tag = Table(
    "post_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

post_o2m_comment = Table(
    "post_o2m_comment",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE")),
    Column("comment_id", Integer, ForeignKey(
        "comments.id", ondelete="CASCADE")),
)