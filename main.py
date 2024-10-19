from fastapi import FastAPI, Depends
from scheme import *
from db import get_db
from service import *


app = FastAPI()


@app.get("/")
def health_check():
    return {"Message": "Hello World"}


@app.get("/user")
def get_weight(username: str, db: Session = Depends(get_db)):
    message = get_weight_in_db(username=username, db=db)
    return message


@app.post("/weight")
def create_new_weight(username: str, item: GetNewWeight, db: Session = Depends(get_db)):
    message = create_new_weight_in_db(username=username, data=item, db=db)
    return message


@app.post("/user")
def create_new_user(username: str, item: GetloginData, db: Session = Depends(get_db)):
    message = create_new_user_in_db(username=username, data=item, db=db)
    return message


@app.get("/user/weight")
def weight_change(username: str, db: Session = Depends(get_db)):
    message = get_weight_change(username=username, db=db)
    return message


@app.get("/user/bmi")
def bmi_for_user(username: str, db: Session = Depends(get_db)):
    message = get_bmi_for_user(username=username, db=db)
    return message
