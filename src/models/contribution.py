from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from datetime import datetime
import enum
from src.models.base import Base


class ContributionType(enum.Enum):
    REVIEW = "review"
    SALARY = "salary"
    INTERVIEW = "interview"


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contribution_type = Column(Enum(ContributionType))
    created_at = Column(DateTime, default=datetime.now())
