from django.utils.decorators import async_only_middleware
from aiohttp import ClientSession
from CRUD_app.custom_response import CustomJsonResponse
from api_app import shared




@async_only_middleware
def CookiesCheckMiddleware(get_response):
    async def middleware(request):
        if shared.AIOHTTP_SESSION is None:
            shared.AIOHTTP_SESSION = ClientSession()

        async with shared.AIOHTTP_SESSION.post('http://localhost:8000/api/auth/check-tokens', cookies=request.COOKIES) as resp:
            data = await resp.json()

            if data['meta']['success'] == False:
                return CustomJsonResponse(
                    success=False,
                    description=data['meta']['description'] or '''При попытке проверить токены произошла ошибка на сервере авторизации''',
                    status_code=400
                )
                
            if data['data']:
                request.user = data['data']

            else:
                return CustomJsonResponse(success=False, description='Неизвестная ошибка при попытке проверить токены', status_code=400)
        
        response = await get_response(request)
        return response
    
    return middleware