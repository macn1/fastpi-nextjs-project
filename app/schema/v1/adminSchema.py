from pydantic import BaseModel

class adminCreate (BaseModel):
    
    username:str
    email:str
    password:str
    
class adminLogin(BaseModel):
    
    email:str
    password:str
    