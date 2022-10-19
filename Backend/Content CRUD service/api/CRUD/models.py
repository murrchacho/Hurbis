from djongo import models
from .mixins import MongoDBMixin
from datetime import datetime
from .embedded.vacancy_embedded import *


class ApplicantProfile(MongoDBMixin):
    '''Профиль соискателя'''

    userID = models.CharField(max_length=100,  default='')
    first_name = models.CharField(max_length=20,  default='')
    last_name = models.CharField(max_length=20, default='')
    profile_image = models.CharField(max_length=1000, default='')

    class Meta:
        db_table = "applicant_profile"


class ApplicantProfileDetails(MongoDBMixin):
    userid = models.IntegerField(default=0)
    third_name = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)    
    tech_stack = models.CharField(max_length=500)   
    portfolio_links = models.CharField(max_length=1000)
    relocation_country = models.BooleanField(default=False)
    relocation_city = models.BooleanField( default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "applicant_profile_details"


class CompanyProfile(MongoDBMixin):
    '''Профиль компании'''

    userID = models.CharField(max_length=100,  default='')
    company = models.CharField(max_length=20,  default='')
    country = models.CharField(max_length=20) 
    city = models.CharField(max_length=20)

    class Meta:
        db_table = "company_profile" 


class CompanyProfileDetails(MongoDBMixin):

    userid = models.IntegerField(default=0)
    email=models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)    

    class Meta:
        db_table = "company_profile_details" 


class HRProfile(MongoDBMixin):
    '''Профиль HR'''

    userID = models.CharField(max_length=100,  default='')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "hr_profile"


class CV(MongoDBMixin):
    userId = models.CharField(max_length=100,  default='')
    body = models.CharField(max_length=1000,  default='Body')
    position = models.CharField(max_length=100,  default='Position')
    work_experience = models.IntegerField(default='')
    required_salary = models.IntegerField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    tech_stack = models.CharField(max_length=500)

    class Meta:
        ordering = ['-created_at']
        db_table = "CV"


class Vacancy(MongoDBMixin):
    companyId = models.CharField(max_length=100,  default='')
    title = models.CharField(max_length=100, default='')
    body = models.CharField(max_length=10000, default='')
    higher_education = models.BooleanField(default=False)
    relocation_help = models.BooleanField(default=False)
    required_work_experiance = models.IntegerField(default=0)
    required_skills = models.CharField(max_length=500, default='')
    work_schedule = models.EmbeddedField(
        model_container = WorkScheduleEmbedded
    )
    position = models.EmbeddedField(
        model_container = PositionEmbedded
    )
    salary = models.EmbeddedField(
        model_container = SalaryEmbedded
    )
    location = models.EmbeddedField(
        model_container = LocationEmbedded
    )
    interview = models.EmbeddedField(
        model_container = InterviewEmbedded
    )
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        #ordering = ['-created_at']
        db_table = "vacancies"

