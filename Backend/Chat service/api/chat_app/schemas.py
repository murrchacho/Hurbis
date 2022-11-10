from email.message import Message
from ninja import Schema
from ninja import ModelSchema
from .models import Messages




class PaginationScheme(Schema):
    current_position: int
    offset: int
