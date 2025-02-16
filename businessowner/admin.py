from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ExportActionMixin
from import_export.formats import base_formats
from import_export import fields, resources
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget 


admin.site.unregister(Group)


class TermsandPolicyAdminForm(forms.ModelForm):
    class Meta:
        model = TermsandPolicy
        fields = ['user', 'terms_and_condition', 'privacy_policy']
        widgets = {
            'terms_and_condition': forms.Textarea(attrs={'class': 'ckeditor'}),
            'privacy_policy': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

class UserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'MindscapeQ'
    admin.site.index_title = "Admin"

class CityResource(resources.ModelResource):
    state_name = fields.Field(
        column_name='state_name',
        attribute='state__name',
        readonly=True  # This field is read-only during import
    )

    class Meta:
        model = Cities
        fields = ('name', 'state_name', 'created_at', 'status')

class CityAdmin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('name', 'state__name', 'status')
    list_per_page = 10
    list_filter = ('status', 'state')
    list_display = ('name', 'state',  'created_at', 'status')
    resource_class = CityResource  # Use the custom resource class
    formats = (base_formats.CSV, base_formats.XLSX, ) 

class StateAdmin(ExportActionMixin, admin.ModelAdmin):
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


class StudentResource(resources.ModelResource):
    batch_name = fields.Field(
        column_name='batch',
        attribute='batch__batch_name',
        readonly=True
    )
    
    standard_name = fields.Field(
        column_name='standard',
        attribute='standard__standard',
        readonly=True
    )
    business_owner_name = fields.Field(
        column_name='business_owner',
        attribute='business_owner__business_name',
        readonly=True
    )

    class Meta:
        model = Students
        fields = ('first_name', 'last_name', 'email', 'contact_no', 'batch', 'standard', 'created_at', 'status', 'business_owner')


class StudentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'batch', 'standard','email','contact_no', 'business_owner', "get_business_type" )
    resource_class = StudentResource
    list_filter = ('business_owner__business_type', 'batch', 'standard')
    formats = (base_formats.CSV, base_formats.XLSX, )

    def has_add_permission(self, request, obj=None):
        return False
    
    @admin.display(description='Business Type', ordering='business_owner__business_type')
    def get_business_type(self, obj):
        return obj.business_owner.business_type

class CompetitiveExamResource(resources.ModelResource):
    business_owner = fields.Field(
        column_name='business_owner',
        attribute='business_owner__business_name',
        readonly=True
    )

    batch_name = fields.Field(
        column_name='batch',
        attribute='batch__batch_name',
        readonly=True
    )
    
    class Meta:
        model = CompetitiveExams
        fields = ('business_owner', 'exam_title', 'batch', 'total_questions', 'time_duration', 'passing_marks', 'total_marks', 'exam_data', 'start_date')


class CompetitiveExamAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('exam_title', 'start_date', 'total_marks', 'total_questions', )
    resource_class = CompetitiveExamResource
    formats = (base_formats.CSV, base_formats.XLSX, )

    def has_add_permission(self, request, obj=None):
        return False
    

class AcademicExamResource(resources.ModelResource):
    business_owner = fields.Field(
        column_name='business_owner',
        attribute='business_owner__business_name',
        readonly=True
    )

    board_name = fields.Field(
        column_name='board',
        attribute='standard__medium_name__board_name',
        readonly=True
    )

    medium_name = fields.Field(
        column_name='medium',
        attribute='standard__medium_name',
        readonly=True
    )

    standard_name = fields.Field(
        column_name='standard',
        attribute='standard__standard',
        readonly=True
    )
    
    class Meta:
        model = AcademicExams
        fields = ('business_owner', 'exam_title', 'board', 'medium', 'standard', 'total_questions', 'time_duration', 'passing_marks', 'total_marks', 'exam_data', 'start_date')


class AcademicExamAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('exam_title', 'start_date', 'total_marks', 'total_questions',) 
    resource_class = AcademicExamResource
    formats = (base_formats.CSV, base_formats.XLSX, )

    def has_add_permission(self, request, obj=None):
        return False
    
    
class TermsandPolicyAdminForm(forms.ModelForm):
    class Meta:
        model = TermsandPolicy
        fields = ['user', 'terms_and_condition', 'privacy_policy']
        widgets = {
            'terms_and_condition': forms.Textarea(attrs={'class': 'django-ckeditor-widget'}),
            'privacy_policy': forms.Textarea(attrs={'class': 'django-ckeditor-widget'}),
        }  

class TermsAndPolicyAdmin(admin.ModelAdmin):
    form = TermsandPolicyAdminForm



admin.site.register(States, StateAdmin)
admin.site.register(Cities, CityAdmin)
admin.site.register(BusinessOwners, BusinessOwnerAdmin)
admin.site.register(Plans)
admin.site.register(Notifications, NotificationAdmin)
admin.site.register(Students, StudentAdmin)
admin.site.register(CompetitiveExams, CompetitiveExamAdmin)
admin.site.register(AcademicExams, AcademicExamAdmin)
admin.site.register(TermsandPolicy, TermsAndPolicyAdmin)