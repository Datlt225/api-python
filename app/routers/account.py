from fastapi import APIRouter, Depends
from sql_app import schemas, crud
from sql_app.database import get_db
from sql_app import models
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/Account',
    tags=['Account'],
    responses={404: {'message': 'Không tìm thấy!'}}
)


@router.get('/', tags=['Account'])
async def root():
    return {'message': 'Root'}


@router.post('/CreateAccount', tags=['Account'])
async def create_account(account: schemas.CreateAccountRequest, db: Session = Depends(get_db)):
    if crud.create_account(db, account):
        return {'message': 'Tạo tài khoản thành công!'}
    return {'message': 'Email đã tồn tại, vui lòng kiểm tra lại!'}
