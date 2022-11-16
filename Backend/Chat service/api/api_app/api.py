from ninja import NinjaAPI
from chat_app.api import router as auth_router

api = NinjaAPI()

api.add_router("chats", auth_router)