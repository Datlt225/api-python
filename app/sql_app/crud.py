from sqlalchemy.orm import Session
from sql_app import models, schemas


def create_account(db: Session, account: schemas.CreateAccountRequest):
    if db.query(models.User).filter_by(email=account.email).first() is not None:
        return False
    db_user = models.User(email=account.email, password=account.password, name=account.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True


def get_banner(db: Session):
    return [e.__dict__ for e in db.query(models.Banner).all()]
