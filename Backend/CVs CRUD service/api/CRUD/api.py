from datetime import datetime
from ninja import Router
from . import models, schemas
from typing import List
from asgiref.sync import sync_to_async
import json
from django.http import HttpResponse



router = Router()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@router.post("")
async def create(request, payload: schemas.CVInScheme):
    #cv = models.CV()
    #for attr, value in payload.dict().items():
    #    setattr(cv, attr, value)
    #cv.save()
    await models.CV.objects.acreate(**payload.dict())
    return {"success":True}


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