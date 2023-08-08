from django.contrib import admin
from .models import *
# from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ExportActionMixin

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
# admin.site.register(CompetitiveQuestions)
# admin.site.register(CompetitiveBatches)
# admin.site.register(CompetitiveChapters)
# admin.site.register(CompetitiveSubjects)
# admin.site.register(Options)
# admin.site.register(CompetitiveExams)
# admin.site.register(CompetitiveExamData)
admin.site.register(Notifications, NotificationAdmin)


class StudentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_no' )

class CompetitiveExamAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('exam_title', 'start_date', 'total_marks', 'total_questions', 'batch' )

class AcademicExamAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('exam_title', 'start_date', 'total_marks', 'total_questions',) 

admin.site.register(Students, StudentAdmin)
admin.site.register(CompetitiveExams, CompetitiveExamAdmin)
admin.site.register(AcademicExams, AcademicExamAdmin)