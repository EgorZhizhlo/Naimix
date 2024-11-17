from fastapi import FastAPI
from .authentication import auth_router
from .account import account_router

app = FastAPI()


@app.get('/', tags=['Главная страница'])
async def home():
    return {
        'Message': 'API NAIMIX HACKATON'
    }

app.include_router(auth_router)
app.include_router(account_router)
