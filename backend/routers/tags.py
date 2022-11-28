from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .auth import get_db

import sys
sys.path.append('..')

from models import Tag

router = APIRouter(prefix='/api/tags', tags=['tags'])


@router.get('/')
async def get_all_tags(db: Session = Depends(get_db)):
    return db.query(Tag).order_by(Tag.id).all()


@router.get('/{tag_id}/')
async def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=400, detail='tag does not exist')
    return tag
