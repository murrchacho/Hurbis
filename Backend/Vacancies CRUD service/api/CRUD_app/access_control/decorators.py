from functools import wraps
from CRUD_app.custom_response import CustomJsonResponse




def company_only(func):
    @wraps(func)
    async def inner(request, *args, **kwargs):
        if request.user['account_type'] != 'company':
            return CustomJsonResponse(success=False, status_code=400, description="Вы не имеете прав на доступ")
        response = await func(request, *args, **kwargs)
        return response
    return inner


def company_or_hr_only(func):
    @wraps(func)
    async def inner(request, *args, **kwargs):
        if request.user['account_type'] != ('company' or 'hr'):
            return CustomJsonResponse(success=False, status_code=400, description="Вы не имеете прав на доступ")
        response = await func(request, *args, **kwargs)
        return response
    return inner


def applicant_only(func):
    @wraps(func)
    async def inner(request, *args, **kwargs):
        if request.user['account_type'] != 'applicant':
            return CustomJsonResponse(success=False, status_code=400, description="Вы не имеете прав на доступ")
        response = await func(request, *args, **kwargs)
        return response
    return inner