from fastapi import FastAPI, Depends
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


@app.get("/user")
def get_all_users_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"data": users}


@app.get("/user/{id}")
def get_a_single_user(
    id: int, qry: Optional[str] = None, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    return {"data": user}


@app.post("/user/create/")
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
