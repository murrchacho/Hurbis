from djongo import models




class SalaryEmbedded(models.Model):
    frm = models.IntegerField(default=0)
    to = models.IntegerField(default=0)
    currency = models.CharField(max_length=3,  default='RUB')

    class Meta:
        abstract=True


class PositionEmbedded(models.Model):
    title = models.CharField(max_length=50, default="")
    level = models.CharField(max_length=20, default="")

    class Meta:
        abstract=True


class MetaEmbedded(models.Model):
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract=True


class LocationEmbedded(models.Model):
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")

    class Meta:
        abstract=True


class InterviewEmbedded(models.Model):
    format = models.CharField(max_length=50, default="")
    stages = models.IntegerField(default=0)

    class Meta:
        abstract=True


class WorkEmbedded(models.Model):
    company_name = models.CharField(max_length=50, default='')
    experiance = models.IntegerField(default=0)    

    class Meta:
        abstract=True


class EducationEmbedded(models.Model):
    university_name = models.CharField(max_length=50, default='')
    degree = models.CharField(max_length=50, default='')

    class Meta:
        abstract=True


class PortfolioLinksEmbedded(models.Model):
    link = models.CharField(max_length=500, default='')
    img = models.CharField(max_length=500, default='')

    class Meta:
        abstract=True


class SkillsEmbedded(models.Model):
    skill = models.CharField(max_length=50, default="")
    level = models.CharField(max_length=50, default="")

    class Meta:
        abstract=True