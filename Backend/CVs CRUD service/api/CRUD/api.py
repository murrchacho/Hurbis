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
async def create(request, payload: schemas.CVInScheme):
    cookies = request.COOKIES
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/api/auth/check-cookies', cookies=cookies) as resp:
            user_info = await resp.json()
    
    if user_info.get("type")=="applicant":
        info = payload.dict()
        info['user_id'] = user_info.get("username")
        await models.CV.objects.acreate(**info)
        return {"success":True}
    return {"success":False}

@router.get("", response=List[schemas.CVOutScheme])
async def read(request):
    return await sync_to_async(list)(models.CV.objects.all())
    
    
@sync_to_async
def update_object(CV):
    return CV.save()

@router.put("/{CV_id}")
async def update(request, CV_id:int, payload: schemas.CVInScheme):
    is_changed = False
    CV = await sync_to_async(models.CV.objects.get)(id=CV_id)
    for attr, value in payload.dict().items():
        if(getattr(CV, attr) != value):
            is_changed = True
            setattr(CV, attr, value)
    if is_changed:
        setattr(CV, 'updated_at', str(datetime.now()))
        await update_object(CV)
        return {"success":True}
    else:
        return {"success":False, "description":"Nothing to update"}


@router.delete("/{CV_id}")
async def delete(request, CV_id:int):
    await models.CV.objects.filter(id=CV_id).adelete()
    return {"success":True}