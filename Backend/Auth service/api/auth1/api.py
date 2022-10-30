import os
from datetime import datetime
import profile
from ninja import Router
from django.middleware import csrf
from . import schemas
from django.contrib.auth import authenticate
from django.http import HttpResponse
from ninja_jwt.tokens import RefreshToken
#from redis.instance import redis_instance
from django.contrib.auth import get_user_model
from api.settings import settings
import jwt
from .models import *
import uuid
from django.http import JsonResponse


User = get_user_model()

router = Router()

@router.post('/registration')
def registration(request, payload: schemas.RegistrationInScheme):
    credentials = payload.dict()
    user = User(username=credentials.get('username'))
    password = credentials.get('password')
    user.set_password(password)
    user.email = credentials.get("email")
    user.save()
    return {"success":True}
    

@router.post('/login')
def login(request, payload: schemas.LoginInScheme):
    credentials = payload.dict()
    username = credentials.get('username', None)
    password = credentials.get('password', None)
    user = authenticate(username=username, password=password)
    if user:
        csrf.get_token(request)
        return set_tokens_for_user(user)


@router.post('/logout')
def logout(request):
    return HttpResponse("Сделаем вид, что мы инвалидировали текущие куки =)")


@router.post('/check-cookies')
def account_type(request):
    userid = jwt.decode(request.COOKIES[settings.SIMPLE_JWT['ACCESS_COOKIE']], os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))['user_id']
    user = User.objects.get(id=userid)
    if user.profile_type == 'company':
        return JsonResponse({"username": user.username, "type": "company"})
    if user.profile_type == 'hr':
        return JsonResponse({"username": user.username, "type": "hr"})
    if user.profile_type == 'applicant':
        return JsonResponse({"username": user.username, "type": "applicant"})
    return {"success": False}


@router.post('/account-type')
def account_type(request, payload: schemas.AccountTypeScheme):
    userid = jwt.decode(request.COOKIES[settings.SIMPLE_JWT['ACCESS_COOKIE']], os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))['user_id']
    user = User.objects.get(id=userid, profile_type='') 
    if payload.type == 'hr' and payload.company_link and payload.company_name and user:
            company = CompanyProfile.objects.filter(company_name = payload.company_name).first()
            if company.link == payload.company_link:
                HRProfile.objects.create(userid=user, companyid=company)
                setattr(user, 'profile_type', 'hr')
                user.save()
                return {"success":True}
    if payload.type == 'company' and payload.company_name and user:
        link = uuid.uuid4()
        CompanyProfile.objects.create(company_name = payload.company_name, link=link, userid=user)
        setattr(user, 'profile_type', 'company')
        user.save()
        return {"success":True}
    if payload.type == 'applicant' and user:
        ApplicantProfile.objects.create(userid=user)
        setattr(user, 'profile_type', 'applicant')
        user.save()
        return {"success":True}
    return {"success":False}


def set_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    response = JsonResponse({"user":user.username, "type":user.profile_type})
    #redis_instance.set(user.id, data["refresh"])
    response = set_cookie(response, 'access' , 'ACCESS_COOKIE', 'ACCESS_TOKEN', data)
    response = set_cookie(response, 'refresh', 'REFRESH_COOKIE', 'ACCESS_TOKEN', data)

    return response


def set_cookie(response, type, cookie_name, token_name, data):
    response.set_cookie(
            key = settings.SIMPLE_JWT[cookie_name],  
            value = data[type],
            expires = settings.SIMPLE_JWT[f'{token_name}_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
    return response