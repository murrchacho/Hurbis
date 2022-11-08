from djongo import models




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


class LocationEmbedded(models.Model):
    country = models.CharField(max_length=50, default='', primary_key=True)
    city = models.CharField(max_length=50, default='')

    class Meta:
        managed=False


class InterviewEmbedded(models.Model):
    format = models.CharField(max_length=50, default='', primary_key=True)
    stages = models.IntegerField(default=0)

    class Meta:
        managed=False


class WorkEmbedded(models.Model):
    company_name = models.CharField(max_length=50, default='', primary_key=True)
    experience = models.IntegerField(default=0)
    description = models.CharField(max_length=500, default='')

    class Meta:
        managed=False


class EducationEmbedded(models.Model):
    university_name = models.CharField(max_length=50, default='', primary_key=True)
    degree = models.CharField(max_length=50, default='')

    class Meta:
        managed=False


class PortfolioLinksEmbedded(models.Model):
    link = models.CharField(max_length=500, default='', primary_key=True)
    img = models.CharField(max_length=500, default='')

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