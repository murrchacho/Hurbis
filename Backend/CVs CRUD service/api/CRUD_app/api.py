from datetime import datetime
from ninja import Router
from . import schemas
from .models import CV, HRLikedCVs
from typing import List
from asgiref.sync import sync_to_async
import json
from CRUD_app.custom_response import CustomJsonResponse
from CRUD_app.access_control.decorators import applicant_only, hr_only




router = Router()


@router.post("/check-existence")
def check_existence(request, payload: schemas.CVCheckExistenseScheme):
    data = payload.dict()
    r = CV.objects.filter(id=data['cv_id'], username=data['username'])
    if r:
        return CustomJsonResponse()
    else: 
        return CustomJsonResponse(success=False)

@router.put("/{CV_id}")
@applicant_only
async def update(request, CV_id:int, payload: schemas.CVInScheme):
    try:
        data = payload.dict()
        data['updated_at'] = str(datetime.now())
        await CV.objects.filter(id=CV_id).aupdate(**data)
        return CustomJsonResponse()

    except CV.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(success=False, description='Похоже, что такого резюме не существует')

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, description='Что-то пошло не так при обновлении резюме')


@router.delete("/{CV_id}")
@applicant_only
async def delete(request, CV_id:int):
    try:
        await CV.objects.filter(id=CV_id, username=request.user['username']).adelete()
        return CustomJsonResponse()
        
    except CV.DoesNotExist as e:
        print(repr(e))
        return CustomJsonResponse(success=False, description='Похоже, что такого резюме не существует')

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, description='Что-то пошло не так при обновлении резюме')


@router.post("")
@applicant_only
async def create(request, payload: schemas.CVInScheme):
    try:
        data = payload.dict()
        data['username'] = request.user['username']
        await CV.objects.acreate(**data)
        return CustomJsonResponse()

    except Exception as e:
        print(repr(e))
        return CustomJsonResponse(success=False, description='Что-то пошло не так при создании резюме')
        
@router.get("", response=List[schemas.CVOutScheme])
@applicant_only
async def read(request):
    try:
        return await sync_to_async(list)(CV.objects.all())

    except Exception as e:
        print(repr(e))
        return None
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)



