from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated

from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(
    db: Annotated[Session, Depends(get_db)],
    user_id: int
):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user

    raise HTTPException(
        status_code=404,
        detail="User was not found"
    )


@router.post('/create')
async def create_user(
        db: Annotated[Session, Depends(get_db)],
        user_create_model: CreateUser,
):
    db.execute(insert(User).values(username=user_create_model.username,
                                   firstname=user_create_model.firstname,
                                   lastname=user_create_model.lastname,
                                   age=user_create_model.age,
                                   slug=slugify(user_create_model.username)))
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_user(
        db: Annotated[Session, Depends(get_db)],
        user_id: int,
        user_update_model: UpdateUser
):
    user = db.scalar(select(User).where(User.id == user_id))

    if user is not None:
        db.execute(update(User).where(User.id == user_id).values(
            firstname=user_update_model.firstname,
            lastname=user_update_model.lastname,
            age=user_update_model.age
        ))
        db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'
        }

    raise HTTPException(
        status_code=404,
        detail="User was not found"
    )


@router.delete('/delete')
async def delete_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful!'
        }

    raise HTTPException(
        status_code=404,
        detail="User was not found"
    )

