import os
from urllib import request
import jwt
from typing import Any, Optional, Tuple, Type, Union
from django.contrib.auth import get_user_model
from ninja_jwt.tokens import RefreshToken, Token
from api_app.settings_folder import settings
from .models import CompanyProfile, HRProfile
from .custom_response import CustomJsonResponse
#from redis.instance import redis_instance




User = get_user_model()

class CustomRefreshToken(RefreshToken):
    @classmethod
    async def for_user(cls, user: Type[User]) -> Union["Token", Type["Token"]]:
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        username = getattr(user, 'username')
        account_type = getattr(user, 'account_type')
        
        token = cls()
        token["username"] = username
        token["account_type"] = account_type

        company = None
        if account_type == 'company': 
            company = await CompanyProfile.objects.filter(userid=user.id).afirst()
        elif account_type == 'hr':
            hr = await HRProfile.objects.filter(userid=user.id).select_related('companyid').afirst()
            company = await CompanyProfile.objects.filter(id=hr.companyid.id).afirst()

        if company:
            token['company'] = company.company_name 
        else:
            token['company'] = ""

        return token


def get_user_info_from_cookie(request):
    try:
        if settings.SIMPLE_JWT['ACCESS_COOKIE'] in request.COOKIES:
            token_info = jwt.decode(request.COOKIES[settings.SIMPLE_JWT['ACCESS_COOKIE']], os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))
            user_data = {}
            user_data['username'] = token_info['username']
            user_data['account_type'] = token_info['account_type']
            user_data['company'] = token_info['company']

            return user_data, None
        else:
            return None, 'Пожалуйста, выполните вход в аккаунт'

    except jwt.exceptions.ExpiredSignatureError as e:
        print(repr(e))
        return None, 'Куки не валидны, пожалуйста, выполните вход в аккаунт'


async def return_response_with_cookies(user):
    response = CustomJsonResponse(data={'data':{'username':user.username}, 'meta':{}})
    response = await create_tokens_for_user(user, response)
    return response


async def create_tokens_for_user(user: User, response: CustomJsonResponse) -> CustomJsonResponse:
    '''Создает JWT-токены для пользователя и устанавливает их в response.'''
    try:
        refresh = await CustomRefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        #redis_instance.set(user.id, data["refresh"])
        response = set_cookies(response, 'access' , 'ACCESS_COOKIE', 'ACCESS_COOKIE_HTTP_ONLY', 'ACCESS_TOKEN', data)
        response = set_cookies(response, 'refresh', 'REFRESH_COOKIE', 'AUTH_COOKIE_HTTP_ONLY', 'ACCESS_TOKEN', data)

        return response

    except Exception as e:
        print(repr(e))


def set_cookies(response: CustomJsonResponse, type: str, cookie_name: str, http_only: str, token_name: str, data: dict) -> CustomJsonResponse:
    '''Устанавливает JWT-токены в http-only куки в response.'''
    try:
        response.set_cookie(
                key = settings.SIMPLE_JWT[cookie_name],  
                value = data[type],
                expires = settings.SIMPLE_JWT[f'{token_name}_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT[http_only],
                samesite = None
                )
        return response

    except Exception as e:
        print(repr(e))
