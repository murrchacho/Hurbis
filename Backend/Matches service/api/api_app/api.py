from ninja import NinjaAPI
from matches_app.api import router as matches_router

api = NinjaAPI()

api.add_router("v1", matches_router)