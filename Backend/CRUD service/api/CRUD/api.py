from datetime import datetime
from ninja import Router
from . import models, schemas
from typing import List
from asgiref.sync import sync_to_async
import json




router = Router()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


@router.post("/create")
async def create(request, payload: schemas.VacancyInScheme):
    await models.Vacancy.objects.acreate(**payload.dict())
    return {"success":True}


@router.get("/read/", response=List[schemas.VacancyOutScheme])
async def read(request):
    return await sync_to_async(list)(models.Vacancy.objects.all())
    
    
@sync_to_async
def update_object(vacancy):
    return vacancy.save()

@router.put("/update/{vacancy_id}")
async def update(request, vacancy_id:int, payload: schemas.VacancyInScheme):
    is_changed = False
    vacancy = await sync_to_async(models.Vacancy.objects.get)(id=vacancy_id)
    
    for attr, value in payload.dict().items():
        #print(getattr(vacancy, attr), type(getattr(vacancy, attr)) , value, type(value), value!=getattr(vacancy, attr))
        
        if(getattr(vacancy, attr) != value):
            print(value)
            is_changed = True
            setattr(vacancy, attr, value)

    if is_changed:
        setattr(vacancy, 'updated_at', str(datetime.now()))
        print(vacancy._meta.fields)
        await update_object(vacancy)
        return {"success":True}
    else:
        return {"success":False, "description":"Nothing to update"}


@router.delete("/delete/{vacancy_id}")
async def delete(request, vacancy_id:int):
    await models.Vacancy.objects.filter(id=vacancy_id).adelete()
    return {"success":True}