from django.contrib import admin
from .models import *
# Register your models here.

class CityAdmin(admin.ModelAdmin):
    list_display = ('name','state','created_at', 'status', )
    
class StateAdmin(admin.ModelAdmin):
    list_display = ('name','created_at', 'status',  )
   
class BusinessOwnerAdmin(admin.ModelAdmin):
    list_display = ('business_name','city', 'email', 'contact_no', 'status', )


admin.site.register(States, StateAdmin)
admin.site.register(Cities, CityAdmin)
admin.site.register(BusinessOwners, BusinessOwnerAdmin)
admin.site.register(Plans)