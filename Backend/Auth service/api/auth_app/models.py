from django.db import models
from datetime import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager




class MetaFields(models.Model):
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, MetaFields):
    '''Модель аутентификации и авторизации'''

    username = models.CharField(max_length=100, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=10)
    profile_image = models.CharField(max_length=1000, default='')
    profile_type = models.CharField(max_length=10, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']


class ApplicantProfile(MetaFields):
    '''Профиль соискателя'''

    userid = models.OneToOneField(User, on_delete = models.CASCADE, db_column='userid')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='') 

    class Meta:
        db_table = "applicant_profile"


class CompanyProfile(MetaFields):
    '''Профиль компании'''

    userid = models.OneToOneField(User, on_delete = models.CASCADE, db_column='userid')
    company_name = models.CharField(max_length=30, default='')
    link = models.CharField(max_length=50)

    class Meta:
        db_table = "company_profile" 


class HRProfile(MetaFields):
    '''Профиль hr'''

    userid = models.OneToOneField(User, on_delete = models.CASCADE, db_column='userid')
    companyid = models.ForeignKey(CompanyProfile, on_delete = models.CASCADE, db_column='companyid')
    first_name = models.CharField(max_length=30, default='', null=True)
    last_name = models.CharField(max_length=30, default='', null=True)

    class Meta:
        db_table = "hr_profile"


