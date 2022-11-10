from datetime import datetime
from djongo import models
from .mixins import MongoDBMixin
from .embedded import MessagesEmbedded, UsersEmbedded




class Chat(MongoDBMixin):
    users = models.ArrayField(
        model_container = UsersEmbedded
    )

    created_at = models.DateTimeField(default=datetime.now, null=False)

    class Meta:
        ordering = ['created_at']
        db_table = "chats"


class Messages(MongoDBMixin):
    chat_id = models.IntegerField(null=False) 
    timestamp = models.DateTimeField(default=datetime.now, null=False)
    message = models.EmbeddedField(
        model_container = MessagesEmbedded
    )

    class Meta:
        ordering = ['timestamp']
        db_table = "messages"