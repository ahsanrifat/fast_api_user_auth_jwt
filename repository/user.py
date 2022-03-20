from fastapi import HTTPException, status
import schemas
import models
from database import *
from sqlalchemy.orm import Session
from urllib import response
from hashing import hash_password


def get_all_users(db):
    users = db.query(models.User).all()
    return schemas.UserViewList(status=True, user_list=users)


def delete_an_user(id, db):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": False, "message": f"No user found with id {id}"},
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"status": True, "message": f"User {id} deleted successfully"}


def get_an_single_user(id, db):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status": False, "message": "No user found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": False, "message": f"No user found with id {id}"},
        )
    return user


def update_an_user(id, request_body, db):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": False, "message": f"No user found with id {id}"}
    user.update(
        {
            "name": request_body.name,
            "password": request_body.password,
            "email": request_body.email,
            "is_active": request_body.is_active,
            "type": request_body.type,
        },
        synchronize_session=False,
    )
    db.commit()
    return {"status": True, "message": f"User {id} updated successfully"}


def create_an_user(user, db):
    hashed_password = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        password=hashed_password,
        email=user.email,
        is_active=user.is_active,
        type=user.type,
    )
    # new_user = models.User(user)  # this does not work
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
