from django.db.models.signals import post_save
from django.dispatch import receiver
from library.models import User
from libraryproject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def email_post_save(sender, instance, created, **kwargs):

  if created:
    subject = 'Welcome to Online Library Management System!'
    message = f'Thank you {instance.username} for Registering out portal.'
    recepient = str(instance.email)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
