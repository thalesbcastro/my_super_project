from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_pass = user.password + 'notreallyhashed'
    db_user = models.User(email=user.email, hashed_password=fake_hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    import ipdb
    ipdb.set_trace()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        items = user.items
        db.delete(user)
        for item in items:
            db.delete(item)
        db.commit()
        return True

    return False


def get_items(db: Session, skip: int = 0, limit: int = 100):
    objects = db.query(models.Item).offset(skip).limit(limit).all()
    return objects


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
