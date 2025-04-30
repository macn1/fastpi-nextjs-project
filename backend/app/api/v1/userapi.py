from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.db import get_db
from app.model.v1.usermodels import User
from app.schema.v1.userSchema import usercreate,userLogin,userresponse
from app.utilities.auth import hash_password ,verify_password ,create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/signup')
async def create_user(user: usercreate, db: AsyncSession = Depends(get_db)):
   
    stmt = select(User).where(or_(User.email==user.email,User.mobile==user.mobile))
    result = await db.execute(stmt)
    userExist = result.scalar_one_or_none()
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
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post('/login')
async def loginuser(user: userLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)  # <-- FIX: Add await here
    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.email})
    return {"accessToken": token, "token_type": "bearer"}

@router.get('/',response_model=list[userresponse])
async def getallUsers(db:AsyncSession=Depends(get_db)):
    
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.delete('/{user_id}')
async def deleteUser(user_id:int,db:AsyncSession=Depends(get_db)):
    
    result = await db.execute(select(User).where(User.id==user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user does not exist")
    
    await db.delete(user)
    await db.commit()
    return {"message":f'user with id {user_id} deleted successfully'}
   