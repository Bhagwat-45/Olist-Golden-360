from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.database.database import get_db
from api.database import crud
from api.schemas import schemas

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/{golden_id}", response_model=schemas.CustomerProfile)
async def read_customer(golden_id: str, db: AsyncSession = Depends(get_db)):
    customer = await crud.get_customer_by_id(db, golden_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer golden record not found")
    return customer

@router.get("/segment/{segment}", response_model=List[schemas.CustomerProfile])
async def read_customers_by_segment(
    segment: str, 
    limit: int = Query(100, le=1000), 
    offset: int = 0, 
    db: AsyncSession = Depends(get_db)
):
    # Validate segment input
    valid_segments = ["VIP", "High", "Medium", "Low"]
    if segment not in valid_segments:
        raise HTTPException(status_code=400, detail=f"Invalid segment. Must be one of {valid_segments}")
    
    return await crud.get_customers_by_segment(db, segment, limit, offset)

@router.get("/stats/summary", response_model=schemas.SegmentStats)
async def read_segment_stats(db: AsyncSession = Depends(get_db)):
    stats = await crud.get_segment_statistics(db)
    return stats