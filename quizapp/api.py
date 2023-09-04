from ninja import NinjaAPI
from user.views import router as user
from businessowner.views import router as owner 
from businessowner.academic import router as academic

api = NinjaAPI()

api.add_router("/businessOwner", owner)
api.add_router("/businessOwner", academic)
api.add_router("/user", user)
