from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import os


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Your name'), blank=True, max_length=255)
    is_new_user = models.BooleanField(default=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='media/profile_pics')
    user_bio = models.CharField(_('A short bio'), blank=True, null=True, max_length=300)
    user_goals = models.CharField(_('Your goals'), blank=True, null=True, max_length=255)
    friends_with = models.ManyToManyField('self')  # for future use

    def __str__(self):
        return self.username

    @property
    def profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url

    def absolute_path(self):
        return os.path.relpath(self.profile_pic, settings.MEDIA_ROOT)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def after_first_ifflist(self):
        # a function that will convert is_new_user to False after they have completed their first ifflist
        pass
