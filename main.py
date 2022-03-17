from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


class user(BaseModel):
    name: str
    email: str
    password: str
    is_admin: Optional[bool] = False
    is_super_admin: Optional[bool] = False


app = FastAPI()


# operation get
# path operation decorator
@app.get("/")
# path operation function
def read_root():
    return {"Hello": "World"}


@app.get("/user/{id}")
def get_a_single_user(id: int, qry: Optional[str] = None):
    return {"user": id, "param": qry}


@app.post("/user/create/")
def create_user(user: user):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
