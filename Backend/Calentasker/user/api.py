from ninja import Router

router = Router(tags=["user"])

@router.get("/hello")
def hello(request):
    return {"message": "API at your service"}