from django.utils.decorators import async_only_middleware
from aiohttp import ClientSession
from CRUD_app.custom_response import CustomJsonResponse
from api_app import shared
import json



@async_only_middleware
def CookiesCheckMiddleware(get_response):
    async def middleware(request):

        if shared.AIOHTTP_SESSION is None:
            shared.AIOHTTP_SESSION = ClientSession()

        if 'access_token' in request.COOKIES:
            cached = shared.REDIS_SESSION.get(request.COOKIES['access_token'])
            
            if cached:
                decoded=(cached.decode().replace("'",'"'))
                request.user = json.loads(decoded)
            else:
                async with shared.AIOHTTP_SESSION.post('http://localhost:8000/api/v1/tokens-check', cookies=request.COOKIES) as resp:
                    data = await resp.json()
                    shared.REDIS_SESSION.set(request.COOKIES['access_token'], str(data['data']), ex=60)

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
        else:
            return CustomJsonResponse(success=False)

        response = await get_response(request)
        return response
    
    return middleware