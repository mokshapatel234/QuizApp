from ninja import NinjaAPI

from businessowner.views import router as owner 
from businessowner.academic import router as academic
# from someothermodule.views import router as other_router
api = NinjaAPI()

api.add_router("/businessOwner", owner)
api.add_router("/businessOwner", academic)
# api.add_router("/businessOwner", other_router)