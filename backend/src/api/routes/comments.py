from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models import User, Comment
from src.services.auth import auth_service
from src.core.db import get_db
from src.crud import comments as repository_comments
from src.schemas import comments as schema_comments
from src.core.security import allowed_operation_any_user, allowed_operation_admin_moderator

router = APIRouter(prefix='/posts/comments', tags=['comments'])

@router.post("/", status_code=200,
             response_model=schema_comments.CommentResponse,
             dependencies=[Depends(allowed_operation_any_user)])
async def add_comment(body: schema_comments.CommentModel,
                      current_user: User = Depends(
                          auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
    The add_comment function creates a new comment for an image.
        The function takes in the following parameters:
            body (CommentModel): A CommentModel object containing the information of the comment to be created.
            current_user (User): The user who is making this request, as determined by auth_service.get_current_user().
            db (Session): An SQLAlchemy Session object that will be used to make database queries and commits.

    :param body: schema_comments.CommentModel: Validate the body of the request
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Access the database
    :return: A comment object
    """
    # image: Post | None = await repository_images.get_image_by_id(db=db, image_id=body.image_id)
    # if not image:
    #     raise HTTPException(status_code=404, detail="Image doesn't exist")
    # if image.user_id == current_user.id:
    #     raise HTTPException(status_code=403, detail="You can't comment your own image")
    comment: Comment = await repository_comments.create_comment(body=body, user=current_user, db=db)
    return comment


@router.get("/{comment_id}", status_code=200,
            response_model=schema_comments.CommentResponse,
            dependencies=[Depends(allowed_operation_any_user)])
async def read_comment(comment_id: int,
                       db: Session = Depends(get_db)):
    """
    The read_comment function returns a comment by its id.
        The function will return an HTTP 404 error if the comment doesn't exist.

    :param comment_id: int: Specify the comment id to be read
    :param current_user: User: Get the current user from the database
    :param db: Session: Get a database session from the dependency injection container
    :return: A comment object
    """
    comment: Comment = await repository_comments.get_comment_by_id(comment_id=comment_id, db=db)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment doesn't exist")
    return comment


@router.patch("/{comment_id}", status_code=200,
              response_model=schema_comments.CommentResponse,
              dependencies=[Depends(allowed_operation_any_user)])
async def update_comment(comment_id: int,
                         body: schema_comments.CommentUpdate,
                         current_user: User = Depends(
                             auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The update_comment function updates a comment in the database.
        Args:
            comment_id (int): The id of the comment to update.
            body (schema_comments.CommentUpdate): The updated data for the Comment object, as specified by schema_comments.CommentUpdate().
            current_user (User): The user who is making this request, as determined by auth_service.get_current_user().
            db (Session): An SQLAlchemy Session object that will be used to make database queries and commits.

    :param comment_id: int: Get the comment to update
    :param body: schema_comments.CommentUpdate: Get the body of the comment to be updated
    :param current_user: User: Get the current user from the token
    :param db: Session: Pass the database connection
    :return: A comment object
    """
    # exist_comment: Comment = await repository_comments.get_comment_by_id(comment_id=comment_id, db=db)
    # if not exist_comment:
    #     raise HTTPException(status_code=404, detail="Comment not found")
    # if exist_comment.user_id != current_user.id and current_user.role not in allowed_operation_admin_moderator.allowed_roles:
    #     raise HTTPException(
    #         status_code=403, detail="You don't have access to update others comments")
    updated_comment: Comment = await repository_comments.update_comment(comment_id=comment_id, user=current_user, body=body, db=db)
    return updated_comment


@router.delete("/{comment_id}", status_code=200,
               dependencies=[Depends(allowed_operation_admin_moderator)])
async def delete_comment(comment_id: int,
                         current_user: User = Depends(
                             auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The update_comment function updates a comment by deleting it.
        Args:
            comment_id (int): The id of the comment to be deleted.
            current_user (User): The user who is making the request to delete a comment.  
            db (Session): An SQLAlchemy Session object that will be used to make database queries and commits.

    :param comment_id: int: Get the comment id from the url
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the function
    :return: A dictionary with the deleted comment
    """
    exist_comment: Comment = await repository_comments.get_comment_by_id(comment_id=comment_id, db=db)
    if not exist_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return await repository_comments.remove_comment(comment_id=exist_comment.id, db=db)
     
