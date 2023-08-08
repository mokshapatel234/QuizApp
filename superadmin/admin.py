from django.contrib import admin
from .models import *
# from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class CityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'state__name', 'status',  )
    list_per_page = 10 
    list_filter = ('status', 'state', )
    list_display = ('name','state','created_at', 'status', )

    
class StateAdmin(admin.ModelAdmin):
    search_fields = ('name', 'status' )
    list_per_page = 10  
    list_filter = ('status', )
    list_display = ('name','created_at', 'status',  )
   
class BusinessOwnerAdmin(admin.ModelAdmin):
    search_fields = ('business_name', 'city__name', 'email', 'contact_no', 'status' )
    list_per_page = 10 
    list_filter = ('status', 'city')
    list_display = ('business_name','city', 'email', 'contact_no', 'status', )

class NotificationAdmin(admin.ModelAdmin):
    search_fields = ('title', 'message', 'business_owner__business_name', )
    list_per_page = 10 
    list_display = ('title', 'message', )

admin.site.register(States, StateAdmin)
admin.site.register(Cities, CityAdmin)
admin.site.register(BusinessOwners, BusinessOwnerAdmin)
admin.site.register(Plans)
admin.site.register(Notifications, NotificationAdmin)

