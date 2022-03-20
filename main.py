from fastapi import FastAPI
import database
import models
import uvicorn
from routers import user,item


models.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(item.router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
