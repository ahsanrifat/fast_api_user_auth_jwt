from fastapi import APIRouter, Depends, status, Response
import schemas
from database import *
from sqlalchemy.orm import Session
from typing import Optional
from repository import user

router = APIRouter(prefix="/user", tags=["User APIs"])


@router.get("/", response_model=schemas.UserViewList)
def get_all_users_list(db: Session = Depends(get_db)):
    return user.get_all_users(db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_an_user(id, db: Session = Depends(get_db)):
    return user.delete_an_user(id, db)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserView,
)
def get_a_single_user(
    id: int,
    response: Response,
    qry: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return user.delete_an_user(id, db)
    # return {"data": user}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_an_user(id, request_body: schemas.User, db: Session = Depends(get_db)):
    return user.update_an_user(id, request_body, db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(request_body: schemas.User, db: Session = Depends(get_db)):
    return user.create_an_user(request_body, db)
