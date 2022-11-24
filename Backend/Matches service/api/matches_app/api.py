from datetime import timedelta
import os
import json
from ninja import Router
from .custom_response import CustomJsonResponse
from api_app import shared
from . import schemas
from .models import UserLikedPosts




router = Router()


async def make_request(request, service_link: str, path: str, payload: None | str) -> None:
    async with shared.AIOHTTP_SESSION.post(
        f'{service_link}/{path}',
        cookies=request.COOKIES,
        data=payload.encode()
    ) as response:
        return await response.json()


@router.post("/{int:post_id}")
async def match(request, post_id:int, payload:schemas.PostCheckScheme):
    try:
        payload_data = payload.dict()

        username = request.user['username']
        account_type = request.user['account_type']
        post_author = payload_data['author']
        response = CustomJsonResponse()

        if shared.REDIS_SESSION_LIKED_POSTS.sismember(f"{username}_liked_posts", post_id):
            return CustomJsonResponse(
                success=False,
                description='Пост уже лайкнут',
                status_code=400
            )
        else:
            
            json_obj = {}
            json_obj['username'] = post_author
            json_obj['post_id'] = post_id
            payload = json.dumps(json_obj)

            if account_type == 'applicant':
                if shared.REDIS_SESSION_ACTUAL_VACANCIES.get(post_id):
                    response['meta']['success'] = True
                else:  
                    response = await make_request(
                        request = request,
                        service_link = os.environ.get("VACANCIES_MICROSERVICE_URL"),
                        path = 'check-existence',
                        payload = payload
                    )           
                    if response['meta']['success']: 
                        shared.REDIS_SESSION_ACTUAL_VACANCIES.set(name=post_id, value='', ex=60)

            elif account_type == 'hr' or 'company':
                if shared.REDIS_SESSION_ACTUAL_CVS.get(post_id):
                    response['meta']['success'] = True
                else:
                    response = await make_request(
                        request = request,
                        service_link = os.environ.get("CVS_MICROSERVICE_URL"),
                        path = 'check-existence',
                        payload = payload
                    )
                    if response['meta']['success']:
                        shared.REDIS_SESSION_ACTUAL_CVS.set(name=post_id, value='', ex=60)

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

            posts = await UserLikedPosts.objects.filter(username=username).afirst()
            if posts:
                if not {'post_id':post_id} in posts.liked_posts:
                    liked_posts = posts.liked_posts + [{'post_id':post_id}]
                    await UserLikedPosts.objects.filter(
                        username=username
                    ).aupdate(
                        liked_posts=liked_posts
                    )
            else:
                await UserLikedPosts.objects.acreate(
                    username=username,
                    liked_posts=[{'post_id':post_id}]
                )

            shared.REDIS_SESSION_LIKED_POSTS.sadd(
                f"{username}_liked_posts",
                post_id
            )

        if (
            shared.REDIS_SESSION_LIKED_USERS.sismember(f"{username}_liked_users", post_author) and
            shared.REDIS_SESSION_LIKED_USERS.sismember(f"{post_author}_liked_users", username)
        ):
            payload = json.dumps({
                    'users':
                    [
                        {'username':username},
                        {'username':post_author}
                    ]
                })

            response = await make_request(
                request = request,
                service_link = os.environ.get("CHATS_MICROSERVICE_URL"),
                path = f'create-chat',
                payload = payload
            )
            #Notify-microservice: 'Match уже установлен'

        shared.REDIS_SESSION_LIKED_USERS.sadd(
            f"{username}_liked_users",
            post_author
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