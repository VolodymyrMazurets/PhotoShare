from typing import List

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.models import Comment, User, Post
from src.schemas.comments import CommentBase, CommentModel, CommentUpdate


async def get_comments(
    post_id: int, limit: int, offset: int, db: Session
) -> List[Comment]:
    """
    The get_comments function returns a list of comments for the image with the given id.
    The limit and offset parameters are used to paginate through results.

    :param post_id: int: Filter the comments by post_id
    :param limit: int: Limit the number of comments returned
    :param offset: int: Specify the number of comments to skip before returning the results
    :param db: Session: Pass the database session to the function
    :return: A list of comment objects
    """
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


async def get_comment_by_id(
    comment_id: int, db: Session
) -> Comment | None:
    """
    The get_comment_by_id function returns a comment by its id.

    :param post_id: int: Filter the comments by post_id
    :param comment_id: int: Filter the comments by their id
    :param db: Session: Pass the database session to the function
    :return: A comment object or none
    """
    return (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )


async def create_comment(
    body: CommentModel, user: User, db: Session
) -> Comment | None:
    """
    The create_comment function creates a new comment for an image.

    :param body: CommentBase: Pass in the comment object from the request body
    :param post_id: int: Get the image id from the database
    :param owner: User: Get the user that is making the comment
    :param db: Session: Pass in the database session
    :return: A comment object
    """
    try:
        post = db.query(Post).filter(Post.id == body.post_id).first()
        comment = Comment(user=user, post=post, content=body.content)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    except Exception as err:
        print(f"create_comment {err=}")


async def update_comment(
    comment_id: int, body: CommentUpdate, user: User, db: Session
) -> Comment | None:
    """
    The update_comment function updates a comment in the database.

    :param post_id: int: Identify the image that the comment belongs to
    :param comment_id: int: Filter the comment that is being updated
    :param body: CommentBase: Pass the new comment to the function
    :param owner: User: Check if the user is the owner of the comment
    :param db: Session: Access the database
    :return: A comment object or none
    """
    comment = (
        db.query(Comment)
        .filter(
            and_(
                Comment.id == comment_id,
                Comment.user_id == user.id,
            )
        )
        .first()
    )

    if comment:
        comment.content = body.new_comment
        db.commit()

    return comment


async def remove_comment(
    comment_id: int, db: Session
) -> Comment | None:
    """
    The remove_comment function removes a comment from the database.

    :param post_id: int: Find the image that the comment is on
    :param comment_id: int: Identify the comment to be removed
    :param owner: User: Check if the user is the owner of the comment
    :param db: Session: Access the database
    :return: A comment object or none
    """
    comment = (
        db.query(Comment)
        .filter(
            and_(
                Comment.id == comment_id,
            )
        )
        .first()
    )

    if comment:
        db.delete(comment)
        db.commit()

    return comment


async def get_image_by_id(post_id: int, db: Session):
    """
    The get_image_by_id function returns an image object from the database, given its id.


    :param post_id: int: Specify the id of the image that is being requested
    :param db: Session: Pass the database session to the function
    :return: A single image object from the database
    """
    return db.query(Post).filter(Post.id == post_id).first()
