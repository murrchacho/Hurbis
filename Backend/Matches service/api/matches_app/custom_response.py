import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder




class CustomJsonResponse(HttpResponse):
    '''Класс кастомного JsonResponse. Служит для шаблонизации ответов от сервера.'''
    def __init__(
        self,
        data={'data':{}, 'meta':{}},
        success=True,
        description=None,
        status_code=None,
        allow_null=False,
        encoder=DjangoJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs,
    ):
    
        if data is None:
            data = {'data':{}, 'meta':{}}

        if safe and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
            
        if json_dumps_params is None:
            json_dumps_params = {}
            
        kwargs.setdefault("content_type", "application/json")


        if allow_null == False:
            for _, value in data.items():
                if value is None or '':
                    success = False 
                    break
        
        if success == False and status_code is None:
            status_code = 400

        kwargs.setdefault("status", status_code)
        
        data['meta']['success'] = success
        if description:
            data['meta']['description'] = description

        data = json.dumps(data, cls=encoder, **json_dumps_params)

        super().__init__(content=data, **kwargs)
