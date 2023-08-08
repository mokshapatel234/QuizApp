from django.db import models
from djongo import models
from django.core.validators import FileExtensionValidator, RegexValidator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
import uuid
from django.contrib.auth.models import User


# Create your models here.

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class States(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("State"), max_length=50,unique=True)
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()   


    def delete(self, hard=False, **kwargs):
        if hard:
            super(States, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1. States"


class Cities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.ForeignKey(States, on_delete=models.CASCADE, related_name="state")
    name = models.CharField(("City"), max_length=50,unique=True)
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()   


    def delete(self, hard=False, **kwargs):
        if hard:
            super(Cities, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "2. Cities"

class BusinessOwners(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_name = models.CharField(max_length=50,verbose_name='Business Name')
    CHOICES = (('competitive','competitive'),('academic','academic'))
    business_type = models.CharField(("Business Type"),choices=CHOICES, max_length=50)
    first_name = models.CharField(max_length=50,verbose_name='First Name')
    last_name = models.CharField(max_length=50,verbose_name='Last Name')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=40, verbose_name='Password')
    logo = models.ImageField(blank=True, upload_to="owner", validators=[FileExtensionValidator(['jpg','jpeg','png'])], height_field=None, width_field=None, max_length=None, null=True)
    tution_tagline = models.CharField(max_length=50, null=True, verbose_name='Tution Tagline')
    contact_no = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{10}$")], max_length=10, unique=True, verbose_name='Contact No')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name="owner_city")
    address = models.TextField()
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()   


    def delete(self, hard=False, **kwargs):
        if hard:
            super(BusinessOwners, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.business_name
    
    class Meta:
        verbose_name_plural = "3. Business Owners"

 
class Plans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_name = models.CharField(max_length=50, verbose_name='Plan Name')
    image = models.ImageField(blank=True, upload_to="plan", validators=[FileExtensionValidator(['jpg','jpeg','png'])], height_field=None, width_field=None, max_length=None)
    description = models.TextField()
    price = models.FloatField()
    PLAN_CHOICES = (
    (3, '3 months'),
    (6, '6 months'),
    (9, '9 months'),
    (12, '12 months'),
    )
    validity = models.IntegerField(choices=PLAN_CHOICES,default='3')
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Plans, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.plan_name
    
    class Meta:
        verbose_name_plural = "4. Plans"

class PurchaseHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE, related_name="plan")
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner")
    order_id = models.CharField(max_length=20)
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Plans, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return f"{self.plan.plan_name} ({self.business_owner.first_name} {self.business_owner.last_name})"
    

class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ArrayReferenceField(BusinessOwners, verbose_name='Business Owner')
    title = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Notifications, self).delete()
        else:
            self.deleted_at = now()
            self.save()
            
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "5. Notifications"