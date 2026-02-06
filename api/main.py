from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from api.routers import customer_route
from api.database.database import get_db
import time

app = FastAPI(
    title="Golden 360: Unified Customer API",
    description="Identity Bridge for Olist E-commerce Data",
    version="1.0.0"
)

# Include our nested routers
app.include_router(customer_route.router)

@app.get("/", tags=["General"])
async def root():
    return {
        "project": "Golden 360",
        "status": "Online",
        "docs": "/docs",
        "message": "One API call. Complete customer profile. Milliseconds."
    }

@app.get("/health", tags=["General"])
async def get_health(db: AsyncSession = Depends(get_db)):
    """
    Verified Health Check: Actually pings the database.
    """
    try:
        start_time = time.time()
        # Ping the database
        await db.execute(text("SELECT 1"))
        latency = time.time() - start_time
        
        return {
            "status": "healthy",
            "database": "connected",
            "latency_ms": round(latency * 1000, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Error Handler Example
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {
        "error": "InternalServerError",
        "message": "Something went wrong behind the scenes.",
        "detail": str(exc) if app.debug else "Contact support"
    }