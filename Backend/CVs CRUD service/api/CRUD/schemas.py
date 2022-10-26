from ninja import Schema
from pydantic import BaseModel




class PositionScheme(Schema):
    title: str
    level: str


class LocationScheme(Schema):
    country: str
    city: str


class SalaryScheme(Schema):
    currency: str
    frm: int
    to: int


class WorkExperienceScheme(Schema):
    company_name: str
    experience: int
    description: str


class HigherEducationScheme(Schema):
    university_name: str
    degree: str


class SkillsScheme(Schema):
    skill: str
    level: str

class CVInScheme(Schema):
    user_id: str
    body: str
    position: PositionScheme
    higher_education: list[HigherEducationScheme]
    work_experience: list[WorkExperienceScheme]
    salary: SalaryScheme 
    location: LocationScheme 
    skills: list[SkillsScheme]

    #ToDo: @validator


class CVOutScheme(CVInScheme):
    id: str
    
