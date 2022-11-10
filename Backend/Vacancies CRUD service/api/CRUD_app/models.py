from djongo import models
from .mixins import MongoDBMixin
from datetime import datetime
from .embedded import *




class Vacancy(MongoDBMixin):
    '''Модель поста с вакансией'''
    user_id = models.CharField(max_length=100, null=False)
    body = models.CharField(max_length=10000, default='')
    position = models.EmbeddedField(
        model_container = PositionEmbedded
    )
    higher_education = models.BooleanField(default=False)
    relocation_help = models.BooleanField(default=False)
    required_work_experiance = models.IntegerField(default=0)
    work_schedule = models.EmbeddedField(
        model_container = WorkScheduleEmbedded
    )
    interview = models.EmbeddedField(
        model_container = InterviewEmbedded
    )
    required_skills = models.ArrayField(
        model_container = SkillsEmbedded
    )
    salary = models.EmbeddedField(
        model_container = SalaryEmbedded
    )
    location = models.EmbeddedField(
        model_container = LocationEmbedded
    )
    
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created_at']
        db_table = "vacancies"


class ApplicantLikedVacancies(MongoDBMixin):
    username = models.CharField(max_length=100, null=False)
    liked_vacancies = models.ArrayField(
        model_container = LikedVacanciesEmbedded
    )

    created_at = models.DateTimeField(default=datetime.now, null=False)

    class Meta:
        ordering = ['created_at']
        db_table = "applicant_liked_vacancies"