from ninja import NinjaAPI
from user.api import router as user_router

api = NinjaAPI(title="Calentasker API -- Docs", version="1.0.0", description="API for Calentasker")

api.add_router("/user/", user_router)