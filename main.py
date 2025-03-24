from fastapi import FastAPI
from database import Base, engine
from route import router
import uvicorn

# Base.metadata.create_all(bind=engine)

APP=FastAPI()
APP.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:APP", host="0.0.0.0", port=8000)