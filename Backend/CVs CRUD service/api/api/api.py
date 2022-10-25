from ninja import NinjaAPI
from CRUD.api import router as CRUD_router

api = NinjaAPI()

api.add_router("cvs/", CRUD_router)