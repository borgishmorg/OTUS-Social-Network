from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.dependencies.database import pools_lifespan
from backend.handlers.login import login
from backend.handlers.user_get import user_get
from backend.handlers.user_register import user_register
from backend.handlers.user_search import user_search


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with pools_lifespan():
        yield


app = FastAPI(lifespan=lifespan)

app.add_api_route('/login', login, methods=['POST'])
app.add_api_route('/user/register', user_register, methods=['POST'])
app.add_api_route('/user/get/{user_id}', user_get, methods=['GET'])
app.add_api_route('/user/search', user_search, methods=['GET'])
