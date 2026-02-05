from fastapi import FastAPI
from api.routers import customer_route

app = FastAPI(title="A Golden Customer 360 API")

app.include_router(customer_route.router)

@app.get("/")
def root():
    return {
        "message" : "Welcome!"
        }

@app.get("/health")
def get_health():
    return {
        "Okay"
    }