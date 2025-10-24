from fastapi import FastAPI
from http import HTTPStatus

# Importe o router que criamos
from .routers import items 
from .schemas import Message

app = FastAPI()

# Inclua o router na aplicação principal
app.include_router(items.router) 

@app.get('/', status_code=HTTPStatus.OK, response_model=Message, include_in_schema=False)
def read_root():
    return {'message': 'CSV Reader API is running!'}