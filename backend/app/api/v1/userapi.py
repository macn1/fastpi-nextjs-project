from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schema import usercreate,userLogin
from app.utilities.auth import hash_password ,verify_password ,create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/signup')
def create_user(user: usercreate, db: Session = Depends(get_db)):
    userExist = db.query(User).filter(
        (User.email == user.email) | (User.mobile == user.mobile)
    ).first()

    if userExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this Email or Phone already exists")

    hashed_pwd = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_pwd,
        email=user.email,
        mobile=user.mobile
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')

def loginuser(user:userLogin,db:Session=Depends(get_db)):
    
    db_user = db.query(User).filter(user.email==User.email).first()
    
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")

    token = create_access_token(data={"sub": db_user.email})
    
    return {"accessToken":token,"token_type":"bearer"}