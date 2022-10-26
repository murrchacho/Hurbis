from ninja import Schema




class PositionScheme(Schema):
    title: str
    level: str


class LocationScheme(Schema):
    country: str
    city: str
    address: str


class SalaryScheme(Schema):
    currency: str
    frm: int
    to: int


class InterviewScheme(Schema):
    format: str
    stages: int


class CommonScheduleScheme(Schema):
    type: str
    schedule: str


class WorkScheduleScheme(Schema):
    in_person_schedule: CommonScheduleScheme
    remote_schedule: CommonScheduleScheme


class SkillsScheme(Schema):
    skill: str
    level: str


class VacancyInScheme(Schema):
    user_id: str
    body: str
    position: PositionScheme
    higher_education: bool
    relocation_help: bool
    required_work_experiance: int
    salary: SalaryScheme 
    location: LocationScheme 
    required_skills: list[SkillsScheme]
    work_schedule: WorkScheduleScheme 
    interview: InterviewScheme 
    #ToDo: @validator


class VacancyOutScheme(VacancyInScheme):
    id: str
    
