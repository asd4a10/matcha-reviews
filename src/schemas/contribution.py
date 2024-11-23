from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ContributionType(str, Enum):
    REVIEW = "review"
    SALARY = "salary"
    INTERVIEW = "interview"


class ContributionCreate(BaseModel):
    contribution_type: ContributionType


class ContributionResponse(ContributionCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
