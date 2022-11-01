from datetime import datetime
from ninja import Router
from . import models, schemas
from typing import List
from asgiref.sync import sync_to_async
import json
from .decorators.company_check import company_hr_only



router = Router()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

@company_hr_only
@router.post("")
async def create(request, payload: schemas.VacancyInScheme):
    data = payload.dict()
    data['user_id'] = request.user['username']
    await models.Vacancy.objects.acreate(**data)
    return {"success":True}

@company_hr_only
@router.get("", response=List[schemas.VacancyOutScheme])
async def read(request):
    await sync_to_async(list)(models.Vacancy.objects.all())
    return {"success":True}
    
    
@sync_to_async
def update_object(vacancy):
    return vacancy.save()

@company_hr_only
@router.put("/{vacancy_id}")
async def update(request, vacancy_id:int, payload: schemas.VacancyInScheme):
    is_changed = False
    vacancy = await sync_to_async(models.Vacancy.objects.get)(id=vacancy_id)
    for attr, value in payload.dict().items():
        if(getattr(vacancy, attr) != value):
            is_changed = True
            setattr(vacancy, attr, value)
    if is_changed:
        setattr(vacancy, 'updated_at', str(datetime.now()))
        await update_object(vacancy)
        return {"success":True}
    else:
        return {"success":False, "description":"Nothing to update"}


@company_hr_only
@router.delete("/{vacancy_id}")
async def delete(request, vacancy_id:int):
    await models.Vacancy.objects.filter(id=vacancy_id, user_id=request.user['username']).adelete()
    return {"success":True}


@router.post("/like/{vacancy_id}")
async def like(request, vacancy_id:int):
    await models.Vacancy.objects.get(id=vacancy_id)
    return {"success":True}