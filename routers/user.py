from fastapi import APIRouter, Depends, HTTPException, status, Response
import schemas
import models
from database import *
from sqlalchemy.orm import Session
from urllib import response
from hashing import hash_password
from typing import Optional

router = APIRouter()

# operation get
# path operation decorator
@router.get("/")
# path operation function
def read_root():
    return {"Hello": "World"}


@router.get("/user", response_model=schemas.UserViewList, tags=["user"])
def get_all_users_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    # return users
    # return {"data": users}
    return schemas.UserViewList(status=True, user_list=users)


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
def delete_an_user(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return {"status": True, "message": f"User {id} deleted successfully"}


@router.get(
    "/user/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserView,
    tags=["user"],
)
def get_a_single_user(
    id: int,
    response: Response,
    qry: Optional[str] = None,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status": False, "message": "No user found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": False, "message": f"No user found with id {id}"},
        )
    return user
    # return {"data": user}


@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["user"])
def update_an_user(id, request_body: schemas.User, db: Session = Depends(get_db)):
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


@router.post("/user/create/", status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
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
