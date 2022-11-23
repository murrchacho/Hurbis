import os
import json
from ninja import Router
from .custom_response import CustomJsonResponse
from api_app import shared
from . import schemas





router = Router()


async def make_request(request, service_link: str, path: str, payload: None | str) -> None:
    async with shared.AIOHTTP_SESSION.post(
        f'{service_link}/{path}',
        cookies=request.COOKIES,
        data=payload.encode()
    ) as response:
        return await response.json()


@router.post('/{int:post_id}')
async def match(request, post_id:int, payload:schemas.PostCheckScheme):
    try:
        payload_data = payload.dict()

        username = request.user['username']
        account_type = request.user['account_type']
        user_for_match = payload_data['author']
        response = {'data':{}, 'meta':{'success':{}, 'description':{}}}

        if shared.REDIS_SESSION.sismember(f"{username}_liked_posts", post_id):
            return CustomJsonResponse(
                success=False,
                description='Пост уже лайкнут',
                status_code=400
            )

        if (
            shared.REDIS_SESSION.sismember(f"{username}_liked_users", user_for_match) and
            shared.REDIS_SESSION.sismember(f"{user_for_match}_liked_users", username)
        ):
            payload = json.dumps({
                    'users':
                    [
                        {'username':username},
                        {'username':user_for_match}
                    ]
                })

            response = await make_request(
                request = request,
                service_link = os.environ.get("CHATS_MICROSERVICE_URL"),
                path = f'create-chat',
                payload = payload
            )
            #Notify-microservice: 'Match уже установлен'

        json_obj = {}
        json_obj['username']=user_for_match
        json_obj['cv_id']=post_id
        payload = json.dumps(json_obj)

        if account_type == 'applicant':
            response = await make_request(
                request = request,
                service_link = os.environ.get("VACANCIES_MICROSERVICE_URL"),
                path = 'check-existence',
                payload = payload
            )
        elif account_type == 'hr' or 'company':
            response = await make_request(
                request = request,
                service_link = os.environ.get("CVS_MICROSERVICE_URL"),
                path = 'check-existence',
                payload = payload
            )
        else:
            return CustomJsonResponse(
                success=False,
                description='Отказано в доступе',
                status_code=400
            )     

        if response['meta']['success'] == False:
            return CustomJsonResponse(
                success=False,
                description=
                '''При попытке проверить существование поста 
                произошла ошибка на стороне сервера''',
                status_code=400
            )

        shared.REDIS_SESSION.sadd(
            f"{username}_liked_posts",
            post_id
        )
        shared.REDIS_SESSION.sadd(
            f"{username}_liked_users",
            user_for_match
        )

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Неизвестная ошибка при попытке установить match'
        )



@router.post("/update_cache/{str:post_id}")
async def update_cache(request):
    pass