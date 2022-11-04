import os
import uuid
import jwt
from django.middleware import csrf
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from . import schemas
from ninja import Router
from api_app.settings_folder import settings
from .models import *
from .custom_response import CustomJsonResponse
from .cookies import return_response_with_cookies, get_info_from_cookies
#from redis.instance import redis_instance




User = get_user_model()
router = Router()


@router.post('/registration')
async def registration(request, payload: schemas.RegistrationInScheme):
    try:
        credentials = payload.dict()
        user, error = await User.objects.registration(credentials)

        if user:
            return await return_response_with_cookies(user)
        
        return CustomJsonResponse(success=False, status_code=400, description=error)

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Что-то пошло не так при регистрации..')
    

@router.post('/login')
async def login(request, payload: schemas.LoginInScheme):
    try:
        credentials = payload.dict()
        user, error = await User.objects.login(credentials)

        if user is None:
            return CustomJsonResponse(success=False, status_code=400, description=error)
           
        csrf.get_token(request) #todo
        return await return_response_with_cookies(user)

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Что-то пошло не так при авторизации..')


@router.post('/logout')
def logout(request):
    return HttpResponse("Сделаем вид, что мы инвалидировали текущие куки =)")


@router.post('/check-cookies')
async def check_cookies(request):
    try:
        userid = jwt.decode(request.COOKIES[settings.SIMPLE_JWT['ACCESS_COOKIE']], os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))['user_id']
        user = await User.objects.aget(id=userid)
        get_info_from_cookies(user)
        return CustomJsonResponse()
    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Возможно, куки не валидны') #ToDo сделать нормальную проверку ошибок


@router.post('/account-type')
def account_type(request, payload: schemas.AccountTypeScheme):
    userid = jwt.decode(request.COOKIES[settings.SIMPLE_JWT['ACCESS_COOKIE']], os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))['user_id']
    user = User.objects.get(id=userid, profile_type='') 
    if user:
        if payload.type == 'hr' and payload.company_link and payload.company_name:
                company = CompanyProfile.objects.filter(company_name = payload.company_name, link=payload.company_link).first()
                HRProfile.objects.create(userid=user, companyid=company)
                setattr(user, 'profile_type', 'hr')
                user.save()
                return {"success":True}
        if payload.type == 'company' and payload.company_name:
            link = uuid.uuid4()
            CompanyProfile.objects.create(company_name=payload.company_name, link=link, userid=user)
            setattr(user, 'profile_type', 'company')
            user.save()
            return {"success":True}
        if payload.type == 'applicant':
            ApplicantProfile.objects.create(userid=user)
            setattr(user, 'profile_type', 'applicant')
            user.save()
            return {"success":True}
    return {"success":False}


