from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BusinessOwners
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=BusinessOwners)
def notify_user(sender, instance, created, **kwargs):
    if created:
        subject = 'Your Business Owner Account Details'
        message = f'Hello {instance.first_name} {instance.last_name},\n\n' \
                  f'Your business owner account for {instance.business_name} has been created.\n' \
                  f'Your login credentials are as per below \n' \
                  f'email: {instance.email}\n' \
                  f'password: {instance.password}\n\n' \
                  f'Thank you!'
        from_email = settings.EMAIL_HOST_USER  # Replace with your email address
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)
