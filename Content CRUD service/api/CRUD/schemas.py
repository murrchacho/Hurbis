from datetime import datetime
from locale import currency
from ninja import Schema




class PositionScheme(Schema):
    title: str
    level: str


class LocationScheme(Schema):
    country: str
    city: str
    address: str


class SalaryRangeScheme(Schema):
    frm: int
    to: int


class SalaryScheme(Schema):
    salary_level: SalaryRangeScheme = None
    currency: str


class InterviewScheme(Schema):
    format: str
    stages: int


class CommonScheduleScheme(Schema):
    type: str
    schedule: str


class WorkScheduleScheme(Schema):
    in_person_schedule: CommonScheduleScheme
    remote_schedule: CommonScheduleScheme


class VacancyInScheme(Schema):
    companyId: str
    title: str
    body: str
    position: PositionScheme
    higher_education: bool
    relocation_help: bool
    required_work_experiance: int
    salary: SalaryScheme 
    location: LocationScheme 
    required_skills: dict 
    work_schedule: WorkScheduleScheme 
    interview: InterviewScheme 



    #ToDo: @validator


class VacancyOutScheme(VacancyInScheme):
    id: str
    
