from ninja import Schema
    
class LogininSchema(Schema):
    email: str
    password: str

class LoginSchema(Schema):
    email: str
    password: str
    message: str
    result:bool
    data: list[LogininSchema]

class ChangePasswordInput(Schema):
    email: str
    old_password: str
    new_password: str
    confirm_password: str

class ChangePasswordOutput(Schema):
    result: bool
    message: str = "Password changed successfully"