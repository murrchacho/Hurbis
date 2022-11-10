from datetime import datetime
from djongo import models
from .mixins import MongoDBMixin




class MessagesEmbedded(MongoDBMixin):
    user = models.CharField(max_length=50, default='', primary_key=True)
    body = models.CharField(max_length=10000, default='')

    class Meta:
        managed=False


class UsersEmbedded(MongoDBMixin):
    username = models.CharField(max_length=50, default='', primary_key=True)

    class Meta:
        managed=False