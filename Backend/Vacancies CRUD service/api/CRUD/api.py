from datetime import datetime
from ninja import Router
from . import models, schemas
from typing import List
from asgiref.sync import sync_to_async
import json
from django.http import HttpResponse
import aiohttp



router = Router()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@router.post("")
async def create(request, payload: schemas.VacancyInScheme):
    cookies = request.COOKIES
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/api/auth/check-cookies', cookies=cookies) as resp:
            user_info = await resp.json()
    
    if user_info.get("type")=="company":
        info = payload.dict()
        info['user_id'] = user_info.get("username")
        await models.Vacancy.objects.acreate(**info)
        return {"success":True}
    return {"success":False}


@router.get("", response=List[schemas.VacancyOutScheme])
async def read(request):
    return await sync_to_async(list)(models.Vacancy.objects.all())
    
    
@sync_to_async
def update_object(vacancy):
    return vacancy.save()

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


@router.delete("/{vacancy_id}")
async def delete(request, vacancy_id:int):
    await models.Vacancy.objects.filter(id=vacancy_id).adelete()
    return {"success":True}