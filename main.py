from urllib import response
from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional
import uvicorn
import schemas
import models
import database
from sqlalchemy.orm import Session

models.Base.metadata.create_all(database.engine)


def get_db():

    db = database.SessionLocal()
    try:
        yield db
    except:
        print("DB session local error")
    finally:
        db.close()


app = FastAPI()


# operation get
# path operation decorator
@app.get("/")
# path operation function
def read_root():
    return {"Hello": "World"}


@app.get("/user", response_model=schemas.UserViewList)
def get_all_users_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    # return users
    # return {"data": users}
    return schemas.UserViewList(status=True, user_list=users)


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_an_user(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return {"status": True, "message": f"User {id} deleted successfully"}


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserView)
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


@app.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED)
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


@app.post("/user/create/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        password=user.password,
        email=user.email,
        is_active=user.is_active,
        type=user.type,
    )
    # new_user = models.User(user)  # this does not work
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
