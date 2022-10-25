from djongo import models
from .mixins import MongoDBMixin
from datetime import datetime
from .embedded import *




class Vacancy(MongoDBMixin, ):
    '''Модель поста с вакансией'''

    userId = models.CharField(max_length=100, null=False)
    higher_education = models.BooleanField(default=False)
    relocation_help = models.BooleanField(default=False)
    required_work_experiance = models.IntegerField(default=0)
    work_schedule = models.EmbeddedField(
        model_container = WorkScheduleEmbedded
    )
    interview = models.EmbeddedField(
        model_container = InterviewEmbedded
    )

    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-created_at']
        db_table = "vacancies"


