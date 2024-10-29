from app.database.models import async_session
from app.database.models import User, Direction, Week, Day,Subject
from sqlalchemy import select
from sqlalchemy.future import select

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User). where(User.tg_id == tg_id))
    
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
        
async def get_directions():
    async with async_session() as session:
        return await session.scalars(select(Direction))
    
async def get_direction_week(direction_id):
    async with async_session() as session:
        return await session.scalars(select(Week).where(Week.category == direction_id))
    
async def get_week_day(week_id):
    async with async_session() as session:
        return await session.scalars(select(Day).where(Day.category == week_id))
    
async def get_day_subject(day_id):
    async with async_session() as session:
        return await session.scalars(select(Subject).where(Subject.category == day_id))
    
async def get_subjects_by_category(subject_category):
    async with async_session() as session:
        result = await session.scalars(
            select(Subject).where(Subject.category == subject_category)
        )
        return result.all()
