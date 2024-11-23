from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_db, get_current_user, require_contribution
from src.models.contribution import ContributionType
from src.services.contribution import record_contribution

router = APIRouter()


@router.get("/reviews/{company_id}", response_model=List[ReviewResponse])
async def get_reviews(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_contribution(ContributionType.REVIEW)),
):
    """Get company reviews (requires review contribution)"""
    if current_user.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only view reviews from your company",
        )

    result = await db.execute(
        select(Review)
        .where(Review.company_id == company_id)
        .order_by(Review.created_at.desc())
    )
    return result.scalars().all()


@router.post("/reviews", response_model=ReviewResponse)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a review and unlock review-related features"""
    # Create review
    db_review = Review(
        company_id=current_user.company_id,
        author_id=current_user.id,
        content=bleach.clean(review.content),
        salary_range=review.salary_range,
        pros=bleach.clean(review.pros) if review.pros else None,
        cons=bleach.clean(review.cons) if review.cons else None,
        rating=review.rating,
        is_anonymous=review.is_anonymous,
    )
    db.add(db_review)

    # Record contribution
    await record_contribution(current_user.id, ContributionType.REVIEW, db)

    await db.commit()
    await db.refresh(db_review)
    return db_review
