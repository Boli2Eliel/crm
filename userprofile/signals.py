#When we register a user we want automatically register his profile too

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from userprofile.models import Userprofile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(staff= instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

#----> cf apps.py for continue : insert below code

"""
    class UserConfig(AppConfig):
        #default_auto_field = 'django.db.models.BigAutoField'
        name = 'user'
    
        def ready(self):
            from user import signals
"""
