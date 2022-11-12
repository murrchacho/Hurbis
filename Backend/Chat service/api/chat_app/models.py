from datetime import datetime
from djongo import models
from .mixins import MongoDBMixin
from .embedded import ContentEmbedded, UsersEmbedded




class Chat(MongoDBMixin):
    users = models.ArrayField(
        model_container = UsersEmbedded
    )

    created_at = models.DateTimeField(default=datetime.now, null=False)

    class Meta:
        ordering = ['created_at']
        db_table = "chats"


class Message(MongoDBMixin):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(default=datetime.now, null=False)
    content = models.EmbeddedField(
        model_container = ContentEmbedded
    )

    class Meta:
        ordering = ['timestamp']
        db_table = "messages"