from sqlalchemy import desc
from sqlalchemy.orm import Session
from scheme import *
from db import get_db
from models import *
from exception import *
from datetime import date
from utility import *


def get_weight_in_db(*, username: str, db: Session):
    user_in_db = db.query(User).filter(User.username == username).first()
    if not user_in_db:
        raise UserNotFoundException()

    user_weight = db.query(WheightEntries).filter(
        WheightEntries.username == username).order_by(desc(WheightEntries.date)).first()
    try:
        return {user_in_db.username: user_weight.weight}
    except:
        raise WeightNotFoundException()


def create_new_weight_in_db(*, username: str, data: GetNewWeight, db: Session):
    user_in_db = db.query(User).filter(User.username == username).first()
    if not user_in_db:
        raise UserNotFoundException()
    user_weight = db.query(WheightEntries).filter(
        WheightEntries.username == username).order_by(desc(WheightEntries.date)).first()
    if not user_weight:
        new_weight = WheightEntries(
            username=username, weight=data.weight, date=data.date)
        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)
        return {"msg": "Weight has been added"}
    elif data.date == date.today():
        db.query(WheightEntries).filter_by(username=username,
                                           date=date.today()).update({"weight": data.weight})
        db.commit()
        return {"msg": "Weight has been changed"}
    user_weight_for_time = db.query(WheightEntries).filter(
        WheightEntries.username == username, WheightEntries.date == data.date).first()
    if not user_weight_for_time:
        new_weight = WheightEntries(
            username=username, weight=data.weight, date=data.date)
        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)
        return {"msg": "Weight has been added"}
    else:
        return {"msg": "This date already has weight"}


def create_new_user_in_db(*, username, data: GetloginData, db: Session):
    user_in_db = db.query(User).filter(User.username == username).first()
    if user_in_db:
        raise UserAlreadyExist()
    hash_password = hashPassword(data.password)
    new_user = User(username=username, password=hash_password,
                    height=data.height)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "user has been created"}


def get_weight_change(*, username, db: Session):
    user_in_db = db.query(User).filter(User.username == username).first()
    if not user_in_db:
        raise UserNotFoundException()
    user_weight_in_db = db.query(WheightEntries).filter(
        WheightEntries.username == username).all()
    if not user_weight_in_db:
        raise WeightNotFoundException()
    elif len(user_weight_in_db) == 1:
        return {"Message": f"User has added weight only 1 time."}
    else:
        last_weight = db.query(WheightEntries).filter(
            WheightEntries.username == username).order_by(desc(WheightEntries.date)).first()
        first_weight = db.query(WheightEntries).filter(
            WheightEntries.username == username).order_by(WheightEntries.date).first()
        weight_change = last_weight.weight-first_weight.weight
        if weight_change > 0:
            return {"Message": f"You take extra {weight_change} kilogram."}
        elif weight_change < 0:
            return {"Message": f"You lose {-(weight_change)} kilogram."}
        else:
            return {"Message": "Your weigt is constant."}


def get_bmi_for_user(*, username, db: Session):
    user_in_db = db.query(User).filter(User.username == username).first()
    if not user_in_db:
        raise UserNotFoundException()
    user_weight_in_db = db.query(WheightEntries).filter(
        WheightEntries.username == username).order_by(desc(WheightEntries.date)).first()
    if not user_weight_in_db:
        raise WeightNotFoundException()
    print(user_weight_in_db.weight)
    bmi = round(user_weight_in_db.weight/user_in_db.height**2, 2)
    if bmi < 18.5:
        return {"Message": f"Your bmi is {bmi}.You are underweigt"}
    elif 18.5 < bmi < 24.9:
        return {"Message": f"Your bmi is {bmi}.You are normal"}
    elif 25 < bmi < 29.9:
        return {"Message": f"Your bmi is {bmi}.You are overweigt"}
    elif 30 < bmi < 34.9:
        return {"Message": f"Your bmi is {bmi}.You are obese class 1"}
    elif 35 < bmi < 39.9:
        return {"Message": f"Your bmi is {bmi}.You are obese class 2"}
    elif 40 < bmi:
        return {"Message": f"Your bmi is {bmi}.You are obese class 3"}
