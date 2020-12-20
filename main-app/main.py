import models
from fastapi import Depends, Form, HTTPException, FastAPI
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

class Stock(BaseModel):
    name: str
    price: int
    availability: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    funds: int

    class Config:
        orm_mode = True

class UserStock(BaseModel):
    user_id: int
    stock_id: str
    total: int

    class Config:
        orm_mode = True

@app.get("/stocks/{stock_id}", response_model=Stock, response_model_include=["name", "price", "availability"])
async def get_stock(stock_id: str, db: Session = Depends(get_db)):
    db_stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if(db_stock):
        return db_stock
    else:
        raise HTTPException(status_code=404, detail="Stock not found")

@app.get("/users/{user_id}", response_model=User, response_model_include=["id", "funds"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if(db_user):
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/deposit", response_model=User)
async def update_user(user_id: int = Form(...), amount: int = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.funds += amount
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/withdraw", response_model=User)
async def update_user(user_id: int = Form(...), amount: int = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.funds -= amount
    if db_user.funds < 0:
        db_user.funds = 0
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/stocks/buy")
async def create_user_stocks(user_id: int = Form(...), stock_id: str = Form(...), total: int = Form(...), upper_bound: int = Form(...), lower_bound: int = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if(db_user):
        if(db_stock):
            if db_stock.price <= upper_bound and db_stock.price >= lower_bound:
                if db_user.funds >= db_stock.price * total:
                    db_user_stock = db.query(models.UserStock).filter(models.UserStock.user_id == user_id).filter(models.UserStock.stock_id == stock_id).first()
                    if(db_user_stock):
                        db_user_stock.total += total
                    else:
                        db_user_stock = models.UserStock(user_id=user_id, stock_id=stock_id, total=total)
                        db.add(db_user_stock)
                    
                    db_user.funds -= db_stock.price * total
                    db_stock.availability -= total
                    db.commit()
                    return "Successful Transaction!"
                else:
                    raise HTTPException(status_code=422, detail="Please Check the user's funds & the stock's availability.")
            else:
                return "The current price is out of bounds, please try again later."
        else:
            raise HTTPException(status_code=404, detail="Stock not found")
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/stocks/sell")
async def delete_user_stocks(user_id: int = Form(...), stock_id: str = Form(...), total: int = Form(...), upper_bound: int = Form(...), lower_bound: int = Form(...), db: Session = Depends(get_db)):
    db_user_stock = db.query(models.UserStock).filter(models.UserStock.user_id == user_id).filter(models.UserStock.stock_id == stock_id).first()
    if(db_user_stock):
        db_stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
        if db_stock.price <= upper_bound and db_stock.price >= lower_bound:
            if(db_user_stock.total >= total):
                db_user_stock.total -= total
                if(db_user_stock.total == 0):
                    db.delete(db_user_stock)
                db_user = db.query(models.User).filter(models.User.id == user_id).first()
                db_stock.availability += total
                db_user.funds += total * db_stock.price
                db.commit()
                return "Sold Successfully!"
            else:
                raise HTTPException(status_code=422, detail="Insufficient quantity to complete the selling request.")
        else:
            return "The current price is out of bounds, please try again later."

    else:
        raise HTTPException(status_code=422, detail="Please make sure that this stock belongs to this user.")
