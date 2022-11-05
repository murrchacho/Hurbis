import os
import jwt
from django.contrib.auth import get_user_model
from ninja_jwt.tokens import RefreshToken
from api_app.settings_folder import settings
from .models import *
from .custom_response import CustomJsonResponse
#from redis.instance import redis_instance




User = get_user_model()


def get_user_from_cookie(request):
    jwt.decode(request.COOKIES[settings.SIMPLE_JWT['ACCESS_COOKIE']], os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))['user_id']


async def return_response_with_cookies(user):
    user_info = await get_info_about_user(user)
    response = CustomJsonResponse(data=user_info)
    response = await create_tokens_for_user(user, response)
    return response


async def create_tokens_for_user(user: User, response: CustomJsonResponse) -> CustomJsonResponse:
    '''Создает JWT-токены для юзера и возвращает их в response.'''
    try:
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        #redis_instance.set(user.id, data["refresh"])
        response = set_cookies(response, 'access' , 'ACCESS_COOKIE', 'ACCESS_TOKEN', data)
        response = set_cookies(response, 'refresh', 'REFRESH_COOKIE', 'ACCESS_TOKEN', data)

        return response

    except Exception as e:
        print(repr(e))


def set_cookies(response: CustomJsonResponse, type: str, cookie_name: str, token_name: str, data: dict) -> CustomJsonResponse:
    '''Устанавливает JWT-токены в http-only куки в response.'''
    try:
        response.set_cookie(
                key = settings.SIMPLE_JWT[cookie_name],  
                value = data[type],
                expires = settings.SIMPLE_JWT[f'{token_name}_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
        return response

    except Exception as e:
        print(repr(e))


async def get_info_about_user(user: User) -> dict:
    '''Возвращает дополнительную информацию о профиле пользователя.'''
    try:
        company: CompanyProfile = None
        data = {}

        if user.profile_type == 'company': 
            company =  await CompanyProfile.objects.aget(userid=user.pk)
        elif user.profile_type == 'hr':
            company =  await HRProfile.objects.aget(userid=user.pk)
        if company:
            data['company'] = company.company_name 

        data['username'] = user.username
        data['profile_type'] = user.profile_type

        return data

    except Exception as e:
        print(repr(e))