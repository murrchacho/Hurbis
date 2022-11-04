import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder




class CustomJsonResponse(JsonResponse):
    '''Класс кастомного JsonResponse с возможностью добавлять поля в уже существующий response. Служит для шаблонизации ответов от сервера.'''
    def __init__(
        self,
        data={},
        success=True,
        description=None,
        status_code=200,
        allow_null=False,
        encoder=DjangoJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs,
    ):
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
        
        self.__init_response(success, status_code, description, data, encoder, **kwargs)

    def __init_response(self, success, status_code, description, data, encoder, **kwargs):
        kwargs.setdefault("status", status_code)
        content = {}
        if data is None:
            content = self.set_status(content, success, description)
            content = json.dumps(content, cls=encoder, **self.json_dumps_params)
        else:
            content = data
            content = self.set_status(content, success, description)
        super().__init__(data=content, **kwargs)

    def add_data(self, data: dict, encoder=DjangoJSONEncoder):
        '''Добавляет данные в content экземпляра класса.'''

        old_content = json.loads(self.content)
        new_content = old_content | data
        self.content = json.dumps(new_content, cls=encoder) 

    def set_status(self, data, success, description):
        data['success'] = success
        if description:
            data['description'] = description
        return data

