from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.db import get_db
from app.model.v1.cartmodels import Cartitem
from app.model.v1.bookmodel import Book
from app.schema.v1.cartschema import AddToCart,UpdateCartItem,UpdateCart
from app.utilities.auth import get_current_user
from sqlalchemy.orm import selectinload

router = APIRouter(prefix='/api/v1/cart',tags=['Cart'])

@router.post('/cart',status_code=201)
async def addtoCart(payload:AddToCart,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):
    
    result = await db.execute(select(Book).where(payload.book_id==Book.id))
    book =  result.scalar_one_or_none()
    
    if not book  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    
    cartdata = await db.execute(select(Cartitem).where(Cartitem.user_id==user.id,Cartitem.book_id==payload.book_id))
    item = cartdata.scalar_one_or_none()
    
    if item:
        item.quantity+=payload.quantity
    else:
        cart_item = Cartitem(user_id=user.id,book_id=payload.book_id,quantity=payload.quantity)
        db.add(cart_item)    
    
    await db.commit()
    return {"message":"item added cart succesfully"}

@router.get('/cart',status_code=200)
async def getallCart(db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):

    stmt = (
        select(Cartitem)
        .options(selectinload(Cartitem.book))
        .where(Cartitem.user_id == user.id)
    )
    result = await db.execute(stmt)
    cart= result.scalars().all()
    
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No item found in the cart")
    return cart


@router.put("/update")
async def update_cart(payload: UpdateCart, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    for item in payload.items:
        result = await db.execute(select(Cartitem).where(
            Cartitem.user_id == user.id, Cartitem.book_id == item.book_id))
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            raise HTTPException(status_code=404, detail=f"Cart item with book_id {item.book_id} not found")

        cart_item.quantity = item.quantity

    await db.commit()
    return {"message": "Cart updated"}

@router.delete('/cart/{bookid}')
async def deleltecartItem(bookid:int,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):
    
    result = await db.execute(select(Cartitem).where(Cartitem.book_id==bookid, Cartitem.user_id == user.id))
    cart_item = result.scalar_one_or_none()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await db.delete(cart_item)
    await db.commit()
    return {"message": "Item removed from cart"}