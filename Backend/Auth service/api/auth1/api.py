from datetime import datetime
from ninja import Router
from django.middleware import csrf
from . import schemas
from django.contrib.auth import authenticate
from django.http import HttpResponse
from ninja_jwt.tokens import RefreshToken
#from redis.instance import redis_instance
from django.contrib.auth import get_user_model
from api.settings import settings




User = get_user_model()

router = Router()

@router.post('/registration')
def registration(request, payload: schemas.RegistrationInScheme):
    credentials = payload.dict()
    user = User(username=credentials.get('username'))
    password = credentials.get('password')
    user.set_password(password)
    user.save()
    return {"success":True}

@router.post('/login')
def login(request, payload: schemas.LoginInScheme):
    data = payload.dict()
    print(data)
    username = data.get('username', None)
    password = data.get('password', None)
    user = authenticate(username=username, password=password)
    print(user)
    if user:
        csrf.get_token(request)
        return set_tokens_for_user(user)


def set_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    response = HttpResponse()
    
    #redis_instance.set(user.id, data["refresh"])
    response = setc(response, 'access' , 'ACCESS_COOKIE', 'ACCESS_TOKEN', data)
    response = setc(response, 'refresh', 'REFRESH_COOKIE', 'ACCESS_TOKEN', data)

    return response


def setc(response, type, cookie_name, token_name, data):
    response.set_cookie(
            key = settings.SIMPLE_JWT[cookie_name],  
            value = data[type],
            expires = settings.SIMPLE_JWT[f'{token_name}_LIFETIME'],
            #secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            #samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                        )
    return response