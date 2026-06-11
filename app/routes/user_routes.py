
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import *
from app.services.user_service import *

router = APIRouter(prefix="/users", tags=["Users"])

ROLES = ["admin", "support", "user"]

@router.get("/", response_model=list[UserResponse])
def list_users(role:str=None,is_active:bool=None,order_by:str=None,db:Session=Depends(get_db)):
    return get_all_users(db, role, is_active, order_by)

@router.get("/{user_id}", response_model=UserResponse)
def get_one_user(user_id:int, db:Session=Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create(data:UserCreate, db:Session=Depends(get_db)):

    if data.role not in ROLES:
        raise HTTPException(400, "Rol no permitido")

    if get_user_by_email(db, data.email):
        raise HTTPException(400, "Email duplicado")

    return create_user(db, data)

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id:int, data:UserUpdate, db:Session=Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    return update_user(db, user, data)

@router.patch("/{user_id}", response_model=UserResponse)
def patch(user_id:int, data:UserPatch, db:Session=Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    if not data.model_dump(exclude_unset=True):
        raise HTTPException(400, "No enviaste datos")

    return patch_user(db, user, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id:int, db:Session=Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    delete_user(db, user)
