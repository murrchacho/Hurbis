from ninja import Schema
from ninja import ModelSchema
from .models import Chat, Message
from ninja import ModelSchema



class PaginationScheme(Schema):
    current_position: int
    offset: int

class UsersScheme(Schema):
    username: str
    
class UsersChatScheme(Schema):
    users: list[UsersScheme]
