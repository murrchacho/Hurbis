import uuid
from django.middleware import csrf
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from . import schemas
from ninja import Router
from .models import *
from .custom_response import CustomJsonResponse
from .cookies import return_response_with_cookies, get_info_about_user
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

        if error:
            return CustomJsonResponse(success=False, status_code=400, description=error)

        csrf.get_token(request) #todo
        return await return_response_with_cookies(user)

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Что-то пошло не так при авторизации..')


@router.post('/logout')
async def logout(request):
    return HttpResponse("Сделаем вид, что мы инвалидировали текущие куки =)")


@router.post('/check-cookies')
async def check_cookies(request):
    '''Валидация кук'''
    try:
        userid = get_user_from_cookie(request)
        user = await User.objects.aget(id=userid)
        get_info_from_cookies(user)
        return CustomJsonResponse()

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Возможно, куки не валидны') #ToDo сделать нормальную проверку ошибок


@router.post('/account-type')
async def account_type(request, payload: schemas.AccountTypeScheme):
    '''Выбор типа аккаунта'''
    try:
        userid = get_user_from_cookie(request)
        user = await User.objects.aget(id=userid, profile_type='') 

        if user:
            if payload.type == 'hr' and payload.company_link and payload.company_name:
                company = await CompanyProfile.objects.aget(company_name = payload.company_name, link=payload.company_link)
                await HRProfile.objects.acreate(userid=user, companyid=company)
                await user.aupdate(profile_type='hr')

            if payload.type == 'company' and payload.company_name:
                link = uuid.uuid4()
                await CompanyProfile.objects.acreate(company_name=payload.company_name, link=link, userid=user)
                await user.aupdate(profile_type='company')

            if payload.type == 'applicant':
                await ApplicantProfile.objects.acreate(userid=user)
                await user.aupdate(profile_type='applicant')

        return CustomJsonResponse()

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Невозможно извлечь пользователя из кук')


