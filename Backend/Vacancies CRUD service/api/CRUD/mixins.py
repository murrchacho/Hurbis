from djongo import models
from api.settings.settings import POSTGRESQL, MONGODB



''' Миксины для добавления поля 'db' в 'params' модели, 
    необходим для роутинга между БД '''


class MongoDBMixin(models.Model):
    class params:
        db=MONGODB
    class Meta:
        abstract = True


class PostgreDBMixin(models.Model):
    class params:
        db=POSTGRESQL
    class Meta:
        abstract = True