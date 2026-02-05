from fastapi import APIRouter

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@router.get("/getCustomer")
def get_customer():
    return "Hello World"