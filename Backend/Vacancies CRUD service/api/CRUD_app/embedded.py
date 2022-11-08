from djongo import models




'''primary_key=True и managed=False необходимы для того, чтобы новый Django не жаловался
 на autofield и abstract model instance соответственно. managed=False не даст создать
 данные моделtq в БД как при abstract=True'''
class SalaryEmbedded(models.Model):
    frm = models.IntegerField(default=0, primary_key=True)
    to = models.IntegerField(default=0)
    currency = models.CharField(max_length=3,  default='RUB')

    class Meta:
        managed=False


class PositionEmbedded(models.Model):
    title = models.CharField(max_length=50, default='', primary_key=True)
    level = models.CharField(max_length=20, default='')

    class Meta:
        managed=False


class MetaEmbedded(models.Model):
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        managed=False


class CommonScheduleEmbedded(models.Model):
    type = models.CharField(max_length=50, default='', primary_key=True)
    schedule = models.CharField(max_length=50, default='')

    class Meta:
        managed=False


class WorkScheduleEmbedded(models.Model):
    in_person_schedule = models.EmbeddedField(
        model_container = CommonScheduleEmbedded,
        primary_key=True
    )
    remote_schedule = models.EmbeddedField(
        model_container = CommonScheduleEmbedded
    )

    class Meta:
        managed=False


class LocationEmbedded(models.Model):
    country = models.CharField(max_length=50, default='', primary_key=True)
    city = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=100, default='')

    class Meta:
        managed=False


class InterviewEmbedded(models.Model):
    format = models.CharField(max_length=50, default='', primary_key=True)
    stages = models.IntegerField(default=0)

    class Meta:
        managed=False


class SkillsEmbedded(models.Model):
    skill = models.CharField(max_length=50, default='', primary_key=True)
    level = models.CharField(max_length=50, default='')

    class Meta:
        managed=False


class LikesEmbedded(models.Model):
    userid = models.CharField(max_length=50, default='', primary_key=True)

    class Meta:
        managed=False