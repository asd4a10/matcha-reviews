from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.permissions import verify_access
from src.models.contribution import ContributionType


async def require_contribution(
    contribution_type: ContributionType,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not await verify_access(current_user.id, contribution_type, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This feature requires a {contribution_type.value} contribution",
        )
    return current_user
