from djongo import models




'''primary_key=True и managed=False необходимы для того, чтобы новый Django не жаловался
 на autofield и abstract model instance соответственно. managed=False не даст создать
 данные моделtq в БД как при abstract=True'''    
class LikedPostsEmbedded(models.Model):
    post_id = models.IntegerField(null=False, primary_key=True)

    class Meta:
        managed=False