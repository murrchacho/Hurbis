from ninja import Schema




class RegistrationInScheme(Schema):
    username: str
    password: str


class LoginInScheme(Schema):
    username: str
    password: str