from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# --- Nested Components for Clean API Output ---

class FinancialMetrics(BaseModel):
    total_spend: float = 0.0
    avg_order_value: float = 0.0
    max_single_order: float = 0.0

class BehavioralMetrics(BaseModel):
    order_count: int = 0
    first_order_date: Optional[datetime] = None
    last_order_date: Optional[datetime] = None
    days_since_last_order: Optional[int] = None

class ProductMetrics(BaseModel):
    total_items: int = 0
    unique_products: int = 0
    favorite_category: Optional[str] = None
    product_diversity: float = 0.0

class SentimentMetrics(BaseModel):
    avg_review_score: float = 0.0
    total_reviews: int = 0

class GeographicMetrics(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# --- Main Response Schema ---

class CustomerProfile(BaseModel):
    golden_id: str
    customer_unique_id: str
    customer_id: str
    ltv_segment: str
    created_at: datetime
    
    # Nested fields
    financial: FinancialMetrics
    behavioral: BehavioralMetrics
    products: ProductMetrics
    sentiment: SentimentMetrics
    geographic: GeographicMetrics

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_flat(cls, obj):
        """
        Custom helper to map the flat Postgres row to our nested Pydantic model.
        We will use this in the CRUD layer.
        """
        return cls(
            golden_id=obj.golden_id,
            customer_unique_id=obj.customer_unique_id,
            customer_id=obj.customer_id,
            ltv_segment=obj.ltv_segment,
            created_at=obj.created_at,
            financial=FinancialMetrics(
                total_spend=obj.total_spend,
                avg_order_value=obj.avg_order_value,
                max_single_order=obj.max_single_order
            ),
            behavioral=BehavioralMetrics(
                order_count=obj.order_count,
                first_order_date=obj.first_order_date,
                last_order_date=obj.last_order_date,
                days_since_last_order=obj.days_since_last_order
            ),
            products=ProductMetrics(
                total_items=obj.total_items,
                unique_products=obj.unique_products,
                favorite_category=obj.favorite_category,
                product_diversity=obj.product_diversity
            ),
            sentiment=SentimentMetrics(
                avg_review_score=obj.avg_review_score,
                total_reviews=obj.total_reviews
            ),
            geographic=GeographicMetrics(
                city=obj.geographic_city,
                state=obj.geographic_state,
                latitude=obj.geographic_lat,
                longitude=obj.geographic_lng
            )
        )

class SegmentStats(BaseModel):
    VIP: int
    High: int
    Medium: int
    Low: int
    total: int