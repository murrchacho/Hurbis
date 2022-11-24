from django.utils.decorators import async_only_middleware
from django.http import parse_cookie
from channels.middleware import BaseMiddleware
from aiohttp import ClientSession
from chat_app.custom_response import CustomJsonResponse
from api_app import shared
import json



@async_only_middleware
def CookiesCheckMiddleware(get_response):
    async def middleware(request):
        if shared.AIOHTTP_SESSION is None:
            shared.AIOHTTP_SESSION = ClientSession()

        async with shared.AIOHTTP_SESSION.post('http://localhost:8000/api/v1/tokens-check', cookies=request.COOKIES) as resp:
            data = await resp.json()

            if data['meta']['success'] == False:
                return CustomJsonResponse(
                    success=False,
                    description=data['meta']['description'] or 'При попытке проверить токены произошла ошибка на сервере авторизации',
                    status_code=400
                )
                
            if data['data']:
                request.user = data['data']

            else:
                return CustomJsonResponse(success=False, description='Неизвестная ошибка при попытке проверить токены', status_code=400)
                
        response = await get_response(request)
        return response
    
    return middleware


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        cookies=None
        for name, value in scope.get("headers", []):
            if name == b"cookie":
                cookies = parse_cookie(value.decode("latin1"))
                break

        if shared.AIOHTTP_SESSION is None:
            shared.AIOHTTP_SESSION = ClientSession()
            
        cookies_to_check = {}
        cookies_to_check['access_token'] = cookies['access_token']
        cookies_to_check['refresh_token'] = cookies['refresh_token']

        async with shared.AIOHTTP_SESSION.post('http://localhost:8000/api/auth/check-tokens', cookies=cookies_to_check) as resp:
            response = await resp.json()   
            scope['user'] = response ['data']

        return await super().__call__(scope, receive, send)