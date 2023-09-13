import math
from fastapi import Depends
from sqlalchemy.orm import Session
from src.models.user import User

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
) -> dict:
    result = db.query(User.id, User.email, User.fullname)\
        .filter(User.deleted == False)\
        .filter(User.id == str(id))\
        .first()

    if result is None:
        return None

    return {
        "id": result.id,
        "email": result.email,
        "fullname": result.fullname
    }