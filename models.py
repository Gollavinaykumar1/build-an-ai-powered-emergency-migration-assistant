# models.py — table prefix: build_an_ai_powered_emergency_migration_
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = "build_an_ai_powered_emergency_migration__items"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, index=True)
    description = Column(String, nullable=True)
    status      = Column(String, default="active")
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
