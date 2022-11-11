from asgiref.sync import sync_to_async
from ninja import Router
from . import schemas
from .models import Chat, Messages
from .custom_response import CustomJsonResponse
#from redis.instance import redis_instance
from djongo import database
import json


router = Router()

@router.get('/get-chats')
def get_chats(request):
    print(Chat.objects.filter(users__contains=[{'username':'user_applicant'}]).first())
    return None

@router.get('/chat-get-messages/{int:chat_id}')
async def chat_get_messages():
    pass

@router.post('/paginate/{int:chat_id}')
async def paginate(request, chat_id: int, payload: schemas.PaginationScheme):
    try:
        data = payload.dict()
        current_position = data['current_position']
        offset = data['offset']
        messages = await sync_to_async(list)(
            Messages.objects.filter(
                chat_id=chat_id
        ).order_by('id').values().all()[current_position:offset])
        current_position = current_position + offset
        result = {'data':{}, 'meta':{}}
        result['data']['current_position'] = current_position
        result['data']['messages'] = messages

        return CustomJsonResponse(data=result)

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Что-то пошло не так при попытке загрузить сообщения..'
        )



