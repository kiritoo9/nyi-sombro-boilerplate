import math
from fastapi import Depends
from sqlalchemy.orm import Session
from src.models.user import User
from sqlalchemy.exc import SQLAlchemyError

async def getUserLists(
    db: Session,
    page: int,
    limit: int,
    keywords: str,
) -> list:

    # Prepare filters
    filters = [User.deleted == False]
    if keywords != "":
        filters.append(User.fullname.ilike(f'%{keywords}%'))

    offset = 0
    if limit > 0 and page > 0:
        offset = (limit * page) - limit

    # Query - User List
    result = db.query(User.id, User.email, User.fullname)\
        .filter(*filters)\
        .limit(limit)\
        .offset(offset)\
        .all()
    
    data = []
    for v in result:
        data.append({
            "id": v.id,
            "email": v.email,
            "fullname": v.fullname,
        })

    return data

async def getUserCount(
    db: Session,
    limit,
    keywords: str | None = None
) -> int:
    # Prepare filters
    filters = [User.deleted == False]
    if keywords != "":
        filters.append(User.fullname.ilike(f'%{keywords}%'))

    # Query - Get Count
    totalPage = 1
    count = db.query(User)\
        .filter(*filters)\
        .count()
    if count > 0 and limit > 0:
        totalPage = math.ceil(count / limit)
    
    return totalPage

async def getUserById(
    db: Session,
    id
) -> any:
    result = db.query(User)\
        .filter(User.deleted == False)\
        .filter(User.id == str(id))\
        .first()

    if result is None:
        return None

    return result

async def getUserByEmail(
    db: Session,
    email,
    id: str | None = None
) -> dict:
    filters = [User.deleted == False, User.email == email]
    if id is not None:
        filters.append(User.id == id)

    result = db.query(User.id, User.email, User.fullname, User.password)\
        .filter(*filters)\
        .first()

    if result is None:
        return None

    return {
        "id": result.id,
        "email": result.email,
        "fullname": result.fullname,
        "password": result.password
    }

async def createUser(
    db: Session,
    data: dict
) -> dict:
    try:
        trx = User(**data)
        db.add(trx)
        db.commit()
        db.refresh(trx)
        return { "message": "success", "success": True }
    except SQLAlchemyError as err:
        db.rollback()
        errorMessage = str(err.__dict__['orig'])
        return { "message": errorMessage, "success": False }

async def updateUser(
    db: Session,
    data
) -> dict:
    try:
        db.merge(data)
        db.commit()
        return { "message": "success", "success": True }
    except SQLAlchemyError as err:
        db.rollback()
        errorMessage = str(err.__dict__['orig'])
        return { "message": errorMessage, "success": False }