from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from src.models.base import Base


class Salary(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    amount = Column(Integer)
    currency = Column(String(3))
    years_of_experience = Column(Integer)
    position = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
