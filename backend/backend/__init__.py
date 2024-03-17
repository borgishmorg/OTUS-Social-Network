from fastapi import FastAPI

from backend.handlers.login import login
from backend.handlers.user_get import user_get
from backend.handlers.user_register import user_register

app = FastAPI()

app.add_api_route('/login', login, methods=['POST'])
app.add_api_route('/user/register', user_register, methods=['POST'])
app.add_api_route('/user/get/{user_id}', user_get, methods=['GET'])
