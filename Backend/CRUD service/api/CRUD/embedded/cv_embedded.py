from djongo import models


class EducationEmbedded(models.Model):
    


    class Meta:
        abstract=True


class CVEmbedded(models.Model):
    body = models.CharField(max_length=1000, null=False)
    position = models.CharField(max_length=100,  null=False)
    work_experience = models.IntegerField(default='')
    required_salary = models.IntegerField(default='')

    class Meta:
        abstract=True