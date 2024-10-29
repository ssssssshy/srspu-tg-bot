from sqlalchemy import BigInteger, String, ForeignKey, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3' )

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    
class Direction(Base):
    __tablename__ = "directions"
    id: Mapped[int] = mapped_column(primary_key=True)
    code:Mapped[str] = mapped_column(String(100))

class Week(Base):
    __tablename__ = "weeks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    category: Mapped[int] = mapped_column(ForeignKey('directions.id'))
    
class Day(Base):
    __tablename__ = "days"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    category: Mapped[int] = mapped_column(ForeignKey('weeks.id'))

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    time: Mapped[str] = mapped_column()
    teacher_name: Mapped[str] = mapped_column(String(70))
    office: Mapped[str] = mapped_column()
    coprus: Mapped[str] = mapped_column(String(5))
    category: Mapped[str] = mapped_column(ForeignKey('days.id'))
    type_of_activity:Mapped[str] = mapped_column(String(25))
    
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    
 