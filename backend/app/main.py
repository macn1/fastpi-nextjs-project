from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import SessionLocal,engine,Base
from app.models import User
from app.schema import usercreate,userLogin,userresponse
from app.utilities.auth import  hash_password,verify_password,create_access_token

Base.metadata.create_all(bind=engine)
app = FastAPI()
router = APIRouter()

def get_db():
    db = SessionLocal()  
    try:
        yield db         
    finally:
        db.close()       

@router.post('/signup')
def createuser(user:usercreate,db:Session = Depends(get_db)):
        
        userExist = db.query(User).filter(User.email==user.email| User.mobile == user.mobile).first()
        
        if userExist:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this Email or Phone already exists")

        hashed_pwd =hash_password(user.password)
        
        new_user = User(
                username = user.username,
                password = hashed_pwd,
                email= user.email , 
                mobile = user.mobile
                
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get('/me')
def get():
        return {"message": "hello"}

app.include_router(router)

