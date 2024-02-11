from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from team.models import Team


def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return 'img/avatar.jpg'


class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team, related_name='userprofiles', blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    # image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images', null=True)
    job_function = models.CharField(max_length=200, null=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)

    def get_active_team(self):
        if self.active_team:
            return self.active_team
        else:
            return Team.objects.filter(members__in=[self.user.id]).first()

    def __str__(self):
        return f'{self.user.username}-Profile'

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
