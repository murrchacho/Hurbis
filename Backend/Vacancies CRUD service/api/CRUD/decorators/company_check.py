from django.http import HttpResponseForbidden
from functools import wraps




def company_hr_only(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.user['type'] != ('company' or 'hr'):
            return HttpResponseForbidden("Вы не имеете прав на доступ")
        response = func(request, *args, **kwargs)
        return response
    return inner