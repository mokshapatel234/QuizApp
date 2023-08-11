from ninja import NinjaAPI


from businessowner.views import router as owner 
# from someothermodule.views import router as other_router
api = NinjaAPI()

api.add_router("/businessOwner", owner)
# api.add_router("/businessOwner", other_router)