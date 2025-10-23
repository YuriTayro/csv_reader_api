from fastapi import FastAPI
from http import HTTPStatus


app = FastAPI()

@app.get("/", status_code=HTTPStatus.OK)
def root():
    return {"message": "CSV Reader API is running!"}

