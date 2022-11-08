from django.utils.decorators import async_only_middleware
import aiohttp
from CRUD_app.custom_response import CustomJsonResponse




@async_only_middleware
def CookiesCheckMiddleware(get_response):
    async def middleware(request):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8000/api/auth/check-tokens', cookies=request.COOKIES) as resp:
                data = await resp.json()

                if data['success'] == False:
                    return CustomJsonResponse(
                        success=False,
                        description=data['description'] or '''При попытке проверить токены произошла ошибка на сервере авторизации''',
                        status_code=400
                    )
                    
                if data['username']:
                    user_info = {key: data[key] for key in data if key != 'success'}
                    request.user = user_info

                else:
                    return CustomJsonResponse(success=False, description='Неизвестная ошибка при попытке проверить токены', status_code=400)
        
        response = await get_response(request)
        return response
    
    return middleware