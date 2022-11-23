from ninja import NinjaAPI
from CRUD_app.api import router as CRUD_router

api = NinjaAPI()

api.add_router("v1", CRUD_router)