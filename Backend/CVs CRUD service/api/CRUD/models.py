from djongo import models
from .mixins import MongoDBMixin
from datetime import datetime
from .embedded import *




class CV(MongoDBMixin):
    '''Модель поста с резюме'''

    user_id = models.CharField(max_length=100, null=False)
    body = models.CharField(max_length=10000, default='')
    position = models.EmbeddedField(
        model_container = PositionEmbedded
    )
    salary = models.EmbeddedField(
        model_container = SalaryEmbedded
    )
    skills = models.ArrayField(
        model_container = SkillsEmbedded
    )
    location = models.EmbeddedField(
        model_container = LocationEmbedded
    )
    higher_education = models.ArrayField(
        model_container = EducationEmbedded
    )
    work_experience = models.ArrayField(
        model_container = WorkEmbedded
    )
    relocation_ready_country = models.BooleanField(default=False)
    relocation_ready_city = models.BooleanField( default=False)
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-created_at']
        db_table = "CVs"
