from asgiref.sync import sync_to_async

from ninja import Router

from . import schemas
from .models import Chat, Message
from .custom_response import CustomJsonResponse
#from redis.instance import redis_instance





router = Router()

@router.get('/get-chats')
def get_chats(request):
    chats = Chat.objects.filter(
        users__in=[{'username':request.user['username']}]
    ).prefetch_related('message_set').all()
    
    response=[]
    for chat in chats:
        messages = chat.message_set.values().all()
        response.append(
            {'chat':chat.id, 'messages':list(messages)}
        )

    return response


@router.post('/create-chat')
async def create_chat(request, payload: schemas.UsersChatScheme):
    data = payload.dict()
    await Chat.objects.acreate(**data)
    return CustomJsonResponse()


@router.post('/paginate/{int:chat_id}')
async def paginate(request, chat_id: int, payload: schemas.PaginationScheme):
    try:
        data = payload.dict()
        current_position = data['current_position']
        offset = data['offset']
        messages = await sync_to_async(list)(
            Message.objects.filter(
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



