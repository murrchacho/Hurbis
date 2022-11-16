from ninja import NinjaAPI
from matches_app.api import router as auth_router

api = NinjaAPI()

api.add_router("matches", auth_router)