from datetime import datetime
from ninja import Router
from . import models, schemas
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


@router.get("/{str:company}", response=List[schemas.VacancyOutScheme])
async def read(request, company: str):
    try:
        return await models.Vacancy.objects.filter(company=request.data[company])
    except:
        return None

    
@router.put("/{int:vacancy_id}")
@company_only
async def update(request, vacancy_id:int, payload: schemas.VacancyInScheme):
    try:
        data = payload.dict()
        data['updated_at'] = str(datetime.now())
        await models.Vacancy.objects.aget(id=vacancy_id).aupdate(**data)
        return {"success":True}
    except:
        return {"success":False}


@router.delete("/{int:vacancy_id}")
@company_only
async def delete(request, vacancy_id:int):
    await models.Vacancy.objects.filter(id=vacancy_id, user_id=request.user['username']).adelete()
    return {"success":True}


@router.post("/like/{int:vacancy_id}")
async def like(request, vacancy_id:int):
    models.Vacancy.objects.aget(id=vacancy_id)
    return {"success":True}


@router.post("")
@company_only
async def create(request, payload: schemas.VacancyInScheme):
    data = payload.dict()
    data['user_id'] = request.user['username']
    await models.Vacancy.objects.acreate(**data)
    return CustomJsonResponse()


@router.get("", response=List[schemas.VacancyOutScheme])
async def read(request):
    try:
        return await sync_to_async(list)(models.Vacancy.objects.all())
    except:
        return None