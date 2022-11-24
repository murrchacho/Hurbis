from djongo import models
from .mixins import MongoDBMixin
from datetime import datetime
from .embedded import *




# Create your models here.
class UserLikedPosts(MongoDBMixin):
    username = models.CharField(max_length=100, null=False)
    liked_posts = models.ArrayField(
        model_container = LikedPostsEmbedded
    )

    created_at = models.DateTimeField(default=datetime.now, null=False)

    class Meta:
        ordering = ['created_at']
        db_table = "user_liked_posts"