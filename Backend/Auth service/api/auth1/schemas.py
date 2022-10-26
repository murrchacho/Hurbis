from ninja import Schema




class RegistrationInScheme(Schema):
    username: str
    password: str
    email: str

class LoginInScheme(Schema):
    username: str
    password: str


class AccountTypeScheme(Schema):
    type: str
    first_name: str = None
    last_name: str = None
    company_link: str = None
    company_name: str = None