from pydantic import BaseModel

class usercreate(BaseModel):
    email:str
    password:str
    mobile:str
    username :str
    
class userLogin(BaseModel):
    email:str
    password:str

class userresponse(BaseModel):
    id : int
    username :str
    mobile:str
    email:str
    
    class Config:
        orm_mode = True