from django.utils.decorators import async_only_middleware
from django.http import HttpResponseForbidden
import aiohttp




@async_only_middleware
def CookiesCheckMiddleware(get_response):
    async def middleware(request):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8000/api/auth/check-cookies', cookies=request.COOKIES) as resp:
                data = await resp.json()
                if data['username'] :
                    request.user = data
                else:
                    return HttpResponseForbidden("Вы не имеете прав на доступ")
        
        response = await get_response(request)
        return response
    

    return middleware