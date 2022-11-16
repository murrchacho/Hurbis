import json
from datetime import datetime
from sre_constants import SUCCESS
from ninja import Router
from django.core.cache import cache
from . import schemas
from .models import Vacancy, ApplicantLikedVacancies
from typing import List
from asgiref.sync import sync_to_async
from CRUD_app.access_control.decorators import applicant_only, company_only, company_or_hr_only
from CRUD_app.custom_response import CustomJsonResponse
from api_app import shared

router = Router()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@router.get("/get-liked-vacancies", response=List[schemas.VacancyOutScheme])
def get_liked_vacancies(request):
    username = request.user['username']
    liked_vacancies = ApplicantLikedVacancies.objects.filter(username=username).values('liked_vacancies')
    ids = [
        item['vacancy_id'] for item in liked_vacancies[0]['liked_vacancies']
    ]
    
    return Vacancy.objects.filter(id__in=ids)

@router.post("/check-existence")
def check_existence(request, payload: schemas.VacancyCheckExistenseScheme):
    data = payload.dict()
    r = Vacancy.objects.filter(id=data['vacancy_id'], username=data['username'])
    if r:
        return CustomJsonResponse()
    else: 
        return CustomJsonResponse(success=False)


@router.put("/{int:vacancy_id}")
@company_only
async def update(request, vacancy_id:int, payload: schemas.VacancyInScheme):
    try:
        data = payload.dict()
        data['updated_at'] = str(datetime.now())
        await Vacancy.objects.filter(id=vacancy_id).aupdate(**data)
        return CustomJsonResponse()

    except Vacancy.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False, 
            description='Похоже, что такой вакансии не существует'
        )

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False, 
            description='Что-то пошло не так при обновлении вакансии'
        )


@router.delete("/{int:vacancy_id}")
@company_only
async def delete(request, vacancy_id:int):
    try:
        await Vacancy.objects.filter(
            id=vacancy_id, 
            username=request.user['username']
        ).adelete()
        return CustomJsonResponse()
        
    except Vacancy.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            description='Похоже, что такой вакансии не существует'
        )

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            description='Что-то пошло не так при обновлении вакансии'
        )


@router.get("/{str:company}", response=List[schemas.VacancyOutScheme])
@applicant_only
async def read(request, company: str):
    try:
        return await Vacancy.objects.filter(
            company=request.data[company]
        )

    except Exception as e:
        print(repr(e))
        return None


@router.post("")
@company_only
async def create(request, payload: schemas.VacancyInScheme):
    try:
        data = payload.dict()
        data['username'] = request.user['username']
        await Vacancy.objects.acreate(**data)
        return CustomJsonResponse()

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            description='Что-то пошло не так при создании вакансии'
        )


@router.get("", response=List[schemas.VacancyOutScheme])
@applicant_only
async def read(request):
    try:
        return await sync_to_async(list)(Vacancy.objects.all())

    except Exception as e:
        print(repr(e))
        return None
        

@router.post("/match/{int:vacancy_id}")
@applicant_only
async def match(request, vacancy_id:int):
    try:
        username = request.user['username']
        vacancy = await Vacancy.objects.filter(id=vacancy_id).afirst()
        applicant_liked_vacancy = await ApplicantLikedVacancies.objects.filter(
                                            username=username
                                        ).afirst()

        shared.REDIS_SESSION.sadd(username, f'{vacancy.username}:{vacancy_id}')

        if vacancy:
            if applicant_liked_vacancy:
                if not {'vacancy_id': vacancy.id} in applicant_liked_vacancy.liked_vacancies:
                    liked_vacancies  = applicant_liked_vacancy.liked_vacancies + [{'vacancy_id':vacancy.id}]
                    await ApplicantLikedVacancies.objects.filter(
                        username=username
                    ).aupdate(
                        liked_vacancies=liked_vacancies)
                else:
                    return CustomJsonResponse(
                        success=False,
                        status_code=400,
                        description='Match для данной вакансии уже установлен'
                    )
            else:
                await ApplicantLikedVacancies.objects.acreate(
                    username=username,
                    liked_vacancies=[{'vacancy_id':vacancy.id}]
                )

            key = f"{username}_{vacancy.username}"
            reverse_key = f"{vacancy.username}_{username}"
            await cache.aadd(key, vacancy_id, timeout=None)

            if await cache.ahas_key(reverse_key):
                await cache.aadd(key, "", timeout=None)
                return "Похоже возникла симпатия =). Создаем чат, направляем сообщения в сервис уведомлений"

            return CustomJsonResponse()

        else:
            return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Похоже, что такой вакансии не существует'
        ) 
            

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(
            success=False,
            status_code=400,
            description='Неизвестная ошибка при попытке установить match для данной вакансии'
        )
