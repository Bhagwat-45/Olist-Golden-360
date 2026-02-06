from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, TIMESTAMP, func
from datetime import datetime
from api.database.database import Base

class UnifiedCustomer(Base):
    __tablename__ = "unified_customer_360"

    # Primary Keys & IDs
    golden_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    customer_unique_id: Mapped[str] = mapped_column(String, nullable=False)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    
    # Financials
    total_spend: Mapped[float] = mapped_column(Numeric, default=0.0)
    avg_order_value: Mapped[float] = mapped_column(Numeric, default=0.0)
    max_single_order: Mapped[float] = mapped_column(Numeric, default=0.0)
    
    # Behavioral
    order_count: Mapped[int] = mapped_column(Integer, default=0)
    first_order_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    last_order_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    days_since_last_order: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Products
    total_items: Mapped[int] = mapped_column(Integer, default=0)
    unique_products: Mapped[int] = mapped_column(Integer, default=0)
    favorite_category: Mapped[str] = mapped_column(String, nullable=True)
    product_diversity: Mapped[float] = mapped_column(Numeric, nullable=True)
    
    # Sentiment & Segmentation
    avg_review_score: Mapped[float] = mapped_column(Numeric, nullable=True)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    ltv_segment: Mapped[str] = mapped_column(String, nullable=False)
    
    # Geographic
    geographic_city: Mapped[str] = mapped_column(String, nullable=True)
    geographic_state: Mapped[str] = mapped_column(String, nullable=True)
    geographic_lat: Mapped[float] = mapped_column(Numeric, nullable=True)
    geographic_lng: Mapped[float] = mapped_column(Numeric, nullable=True)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())