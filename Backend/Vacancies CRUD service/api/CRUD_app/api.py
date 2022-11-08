from datetime import datetime
from ninja import Router
from . import schemas
from .models import Vacancy
from typing import List
from asgiref.sync import sync_to_async
import json
from .decorators.company_check import company_only
from .custom_response import CustomJsonResponse


router = Router()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@router.put("/{int:vacancy_id}")
@company_only
async def update(request, vacancy_id:int, payload: schemas.VacancyInScheme):
    try:
        data = payload.dict()
        data['updated_at'] = str(datetime.now())
        await Vacancy.objects.filter(id=vacancy_id).aupdate(**data)
        return CustomJsonResponse()

    except Vacancy.DoesNotExist:
        return CustomJsonResponse(success=False, description='Похоже, что такой вакансии не существует')
    except:
        return CustomJsonResponse(success=False, description='Что-то пошло не так при обновлении вакансии')


@router.delete("/{int:vacancy_id}")
@company_only
async def delete(request, vacancy_id:int):
    try:
        await Vacancy.objects.filter(id=vacancy_id, user_id=request.user['username']).adelete()
        return CustomJsonResponse()

    except Vacancy.DoesNotExist:
        return CustomJsonResponse(success=False, description='Похоже, что такой вакансии не существует')
    except:
        return CustomJsonResponse(success=False, description='Что-то пошло не так при обновлении вакансии')


@router.get("/{str:company}", response=List[schemas.VacancyOutScheme])
async def read(request, company: str):
    try:
        return await Vacancy.objects.filter(company=request.data[company])
    except:
        return None


@router.post("")
@company_only
async def create(request, payload: schemas.VacancyInScheme):
    try:
        data = payload.dict()
        data['user_id'] = request.user['username']
        await Vacancy.objects.acreate(**data)
        return CustomJsonResponse()
    except:
        return CustomJsonResponse(success=False, description='Что-то пошло не так при создании вакансии')


@router.get("", response=List[schemas.VacancyOutScheme])
async def read(request):
    try:
        return await sync_to_async(list)(Vacancy.objects.all())
    except:
        return None


@router.post("/like/{int:vacancy_id}")
async def like(request, vacancy_id:int):
    Vacancy.objects.aget(id=vacancy_id)
    return {"success":True}