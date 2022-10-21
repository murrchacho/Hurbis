from click import decorators
from .tasks import awaitReturn, cookies_validate
import celery_pubsub
from functools import wraps
import uuid
from api.settings import SIMPLE_JWT




class RequestRelation():
    def __init__(self, request):
        self.request = request
        self.taskID = uuid.uuid4() 
        self.result = None

    def validate(self):
        celery_pubsub.subscribe('auth.cookies.results', awaitReturn(self))
        cookies_validate.apply_async(kwargs={
            'access_cookie':self.request.COOKIES.get(SIMPLE_JWT['ACCESS_COOKIE'], ''),
            'refresh_cookie':self.request.COOKIES.get(SIMPLE_JWT['ACCESS_COOKIE'], ''), 
            'uuid':str(self.taskID)
            })


def tokens_request(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        rr = RequestRelation(args[0])     
        rr.validate()
        print(rr.result)
        response = func(request, *args, **kwargs)
        return response
    return inner