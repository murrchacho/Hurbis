import uuid
from django.middleware import csrf
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from ninja import Router
from . import schemas
from .models import ApplicantProfile, CompanyProfile, HRProfile
from .custom_response import CustomJsonResponse
from .cookies import return_response_with_cookies, get_user_info_from_cookie
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
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Что-то пошло не так при регистрации..'
        )
    

@router.post('/login')
async def login(request, payload: schemas.LoginInScheme):
    credentials = payload.dict()
    user, error = await User.objects.login(credentials)

    if error:
        return CustomJsonResponse(success=False, status_code=400, description=error)

    csrf.get_token(request) #todo
    return await return_response_with_cookies(user)


@router.post('/logout')
async def logout(request):
    return HttpResponse("Сделаем вид, что мы инвалидировали текущие куки =)")


@router.post('/tokens-check')
async def check_tokens(request):
    '''Валидация токенов'''
    try:
        user_info, error = get_user_info_from_cookie(request)

        if error:
            return CustomJsonResponse(success=False, status_code=400, description=error)

        return CustomJsonResponse(data={'data':user_info, 'meta':{}})

    except User.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Похоже, что такого профиля пользователя не существует..')

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, status_code=400, description='Неизвестная ошибка при попытке валидации токенов')


@router.post('/account-type')
async def account_type(request, payload: schemas.AccountTypeScheme):
    '''Выбор типа аккаунта'''
    try:
        userid, error = get_user_info_from_cookie(request)
        if error:
            return CustomJsonResponse(success=False, status_code=400, description=error)

        if userid:
            user = await User.objects.filter(
                id=userid,
                account_type='',
                is_active=True
            ).afirst()

            if user:
                if (
                    payload.account_type == 'hr' 
                    and payload.company_link
                    and payload.company_name
                ):
                    company = await CompanyProfile.objects.filter(
                        company_name = payload.company_name,
                        link=payload.company_link
                    ).afirst()
                    await HRProfile.objects.acreate(userid=user, companyid=company)
                    await User.objects.filter(
                        id=userid, 
                        account_type='', 
                        is_active=True
                    ).aupdate(account_type='hr')

                if (
                    payload.account_type == 'company' 
                    and payload.company_name
                ):
                    link = uuid.uuid4()
                    await CompanyProfile.objects.acreate(
                        company_name=payload.company_name,
                        link=link,
                        userid=user
                    )
                    await User.objects.filter(
                        id=userid,
                        account_type='',
                        is_active=True
                    ).aupdate(account_type='company')

                if payload.account_type == 'applicant':
                    await ApplicantProfile.objects.acreate(userid=user)
                    await User.objects.filter(id=userid,
                        account_type='',
                        is_active=True
                    ).aupdate(account_type='applicant')

                return CustomJsonResponse()
            else:
                return CustomJsonResponse(
                    success=False, 
                    status_code=400, 
                    description=('Возможно, Вы ввели неправильное название компании '
                                'или пытаетесь изменить активный тип профиля')
                )
            
    except User.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False, 
            status_code=400,
            description='Похоже, что такого профиля пользователя не существует..'
        )

    except CompanyProfile.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Похоже, что такого профиля компании не существует..'
        )

    except HRProfile.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Похоже, что такого профиля HR не существует..'
        )

    except ApplicantProfile.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Похоже, что такого профиля соискателя не существует..'
        )
    
    except IntegrityError as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description=('Возможно, Вы ввели неправильное название компании '
                        'или пытаетесь изменить активный тип профиля')
        )
        
    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Что-то пошло не так при выборе типа аккаунта..'
        )



