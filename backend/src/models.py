from sqlalchemy import Column, Integer, func, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import DateTime


metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


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


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    role = Column(String, default="user")
    comments = relationship("Comment", back_populates="user")
    posts = relationship("Post", back_populates="user")


class Tag(BaseModel):
    __tablename__ = "tags"
    name = Column(String, unique=True, index=True)
    posts = relationship("Post", secondary=post_m2m_tag, back_populates="tags")


class Post(BaseModel):
    __tablename__ = "posts"
    title = Column(String, index=True)
    description = Column(String)
    image = Column(String)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=post_m2m_tag, back_populates="posts")
    comments = relationship(
        "Comment", secondary=post_o2m_comment, back_populates="post")


class Comment(BaseModel):
    __tablename__ = "comments"
    content = Column(String)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), default=None)
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
