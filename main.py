from fastapi import FastAPI
from typing import Optional
import uvicorn
import schemas


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
def create_user(user: schemas.user):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
