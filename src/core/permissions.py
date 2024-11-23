from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.contribution import Contribution, ContributionType


async def check_user_contributions(user_id: int, db: AsyncSession) -> dict:
    """Check what features user has unlocked based on contributions"""
    query = select(Contribution).where(Contribution.user_id == user_id)
    result = await db.execute(query)
    contributions = result.scalars().all()

    return {
        "has_review": any(
            c.contribution_type == ContributionType.REVIEW for c in contributions
        ),
        "has_salary": any(
            c.contribution_type == ContributionType.SALARY for c in contributions
        ),
        "has_interview": any(
            c.contribution_type == ContributionType.INTERVIEW for c in contributions
        ),
    }


async def verify_access(
    user_id: int, required_contribution: ContributionType, db: AsyncSession
) -> bool:
    """Verify if user has made required contribution to access feature"""
    query = select(Contribution).where(
        Contribution.user_id == user_id,
        Contribution.contribution_type == required_contribution,
    )
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None
