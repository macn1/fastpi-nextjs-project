from fastapi import HTTPException,status,Depends,APIRouter
from app.model.v1.adminmodels import Admin
from app.schema.v1.adminSchema import adminCreate,adminLogin
from app.db.db import get_db
from sqlalchemy import select , or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.utilities.auth import hash_password,verify_password,create_access_token

router = APIRouter(
    prefix='/admin',
    tags=["Admin"]
)

@router.post('/signup')

async def create_admin(admin:adminCreate,db:AsyncSession =Depends(get_db)):
    print("admin",admin.email)
    stmt = select(Admin).where(Admin.email==admin.email)
    result = await db.execute(stmt)
    adminExist = result.scalar_one_or_none()
    
    if adminExist :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Admin Already exist with this email Id")
    
    hashed_pwd = hash_password(admin.password)
    
    new_admin = Admin(
        username = admin.username,
        email  = admin.email,
        password = hashed_pwd
    )
    
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return new_admin


@router.post('/login')

async def admin_login(admin:adminLogin,db:AsyncSession= Depends(get_db)):
    
    stmt = select(Admin).where(Admin.email==admin.email)
    result = await db.execute(stmt)
    adminExst = result.scalar_one_or_none()
    
    if adminExst is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials , admin doesnt exist")
        
    if not verify_password(admin.password,adminExst.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials , password doesnt match")
    
    
    token = create_access_token(data={"sub":admin.email})
    
    return {"acces_token":token,"token_type":"bearer"}