from typing import Type
from django.contrib.auth.models import BaseUserManager
from django.db.models import Model
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import bcrypt




class UserManager(BaseUserManager):
    use_in_migrations = True

    async def _registration(self, data: dict, **extra_fields) -> tuple[Type[Model], None] | tuple[None, str]:
        '''Создает пользователя в БД.

        Возвращает tuple из модели User и None, если пользователь успешно создан.
        Возвращает tuple из None и str, если произошла ошибка.
        '''
        try:
            extra_fields.setdefault("is_admin", False)
            extra_fields.setdefault("is_superuser", False)

            data = data | extra_fields     
            if not data['email']:
                raise ValueError('The email must be provided')
            data['email'] = self.normalize_email(data['email'])

            password = data['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            data['password'] = hashed.decode()
            
            user = await self.acreate(**data)
            return user, None

        except IntegrityError as e:
            print(repr(e))
            return None, "Пользователь с таким логином или почтой уже есть"

        except Exception as e:
            print(repr(e))
            return None, "Неизвестная ошибка"

    async def _login(self, data) -> tuple[Type[Model], None] | tuple[None, str]:
        try:
            username = data['username']

            user = await self.aget(username=username)
            
            password = data['password'].encode()
            hashed = user.password.encode()

            if bcrypt.checkpw(password, hashed):
                return user, None
                
            return None, 'Неверное имя пользователя или пароль'

        except ObjectDoesNotExist as e:
            print(repr(e))
            return None, "Неверное имя пользователя или пароль"

        except Exception as e:
            print(repr(e))
            return None, "Неизвестная ошибка"

    async def registration(self, data: dict, **extra_fields) -> tuple[Type[Model], None] | tuple[None, str]:
        '''Регистрирует пользователя в системе.
                
        Возвращает tuple с моделью User и None, если пользователь успешно зарегистрирован.
        Возвращает tuple с None, и описанием ошибки, если произошла ошибка.
        '''
        return await self._registration(data, **extra_fields)

    async def login(self, data: dict) -> tuple[Type[Model], None] | tuple[None, str]:
        '''Осуществляет аутентификацию пользователя.
                
        Возвращает tuple с моделью User и None, если пользователь успешно авторизован.
        Возвращает tuple с None, и описанием ошибки, если произошла ошибка.
        '''
        return await self._login(data)

