from fastapi import APIRouter, Depends, HTTPException, status, Response
import schemas
import models
from database import *
from sqlalchemy.orm import Session
from urllib import response
from typing import Optional

router = APIRouter()


@router.post(
    "/item/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ItemView,
    tags=["Item"],
)
def create_item(request: schemas.Item, db: Session = Depends(get_db)):
    new_item = models.Item(
        title=request.title,
        description=request.description,
        owner_id=request.owner_id,
    )
    # new_user = models.User(user)  # this does not work
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
