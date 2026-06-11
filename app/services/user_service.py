
from app.models.user_model import User

def get_all_users(db, role=None, is_active=None, order_by=None):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if order_by == "name":
        query = query.order_by(User.name)

    if order_by == "date":
        query = query.order_by(User.created_at)

    return query.all()

def get_user_by_id(db, user_id):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db, email):
    return db.query(User).filter(User.email == email).first()

def create_user(db, data):
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db, user, data):
    for key, value in data.model_dump().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def patch_user(db, user, data):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db, user):
    db.delete(user)
    db.commit()
