from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from api.models import models
from api.schemas import schemas

async def get_customer_by_id(db: AsyncSession, golden_id: str) -> Optional[schemas.CustomerProfile]:
    query = select(models.UnifiedCustomer).where(models.UnifiedCustomer.golden_id == golden_id)
    result = await db.execute(query)
    db_obj = result.scalar_one_or_none()
    
    if db_obj:
        return schemas.CustomerProfile.from_orm_flat(db_obj)
    return None

async def get_customers_by_segment(
    db: AsyncSession, segment: str, limit: int = 100, offset: int = 0
) -> List[schemas.CustomerProfile]:
    query = (
        select(models.UnifiedCustomer)
        .where(models.UnifiedCustomer.ltv_segment == segment)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    return [schemas.CustomerProfile.from_orm_flat(row) for row in rows]

async def get_segment_statistics(db: AsyncSession):
    # This runs a GROUP BY to get counts for the /stats endpoint
    query = select(
        models.UnifiedCustomer.ltv_segment, 
        func.count(models.UnifiedCustomer.golden_id)
    ).group_by(models.UnifiedCustomer.ltv_segment)
    
    result = await db.execute(query)
    stats = {row[0]: row[1] for row in result.all()}
    
    # Add a total
    stats["total"] = sum(stats.values())
    return stats