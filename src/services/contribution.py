from sqlalchemy.ext.asyncio import AsyncSession
from src.models.contribution import Contribution, ContributionType


async def record_contribution(
    user_id: int, contribution_type: ContributionType, db: AsyncSession
) -> Contribution:
    """Record a user contribution"""
    contribution = Contribution(user_id=user_id, contribution_type=contribution_type)
    db.add(contribution)
    await db.commit()
    await db.refresh(contribution)
    return contribution


# Example usage of checking contributions
@router.get("/companies/{company_id}/salaries")
async def get_company_salaries(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_contribution(ContributionType.SALARY)),
):
    """Get salary information (requires salary contribution)"""
    result = await db.execute(
        select(Salary)
        .where(Salary.company_id == company_id)
        .order_by(Salary.created_at.desc())
    )
    return result.scalars().all()
