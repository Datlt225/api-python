from fastapi import APIRouter, Depends
from sql_app import schemas, crud
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/Music',
    tags=['Music'],
    responses={404: {'message': 'Không tìm thấy!'}}
)


@router.get('/', tags=['Music'])
async def root():
    return {'message': 'Root'}


@router.get('/GetBanner', tags=['Music'])
async def get_banner(db: Session = Depends(get_db)):
    return crud.get_banner(db)
