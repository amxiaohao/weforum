from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    url = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    image = models.FileField(upload_to='profile_images', blank=True)
    picture_url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

    def __unicode__(self):
        return self.user.username

    def get_url(self):
        url = self.url
        if 'http://' not in self.url and 'https://' not in self.url and \
                len(self.url) > 0:
            url = 'http://' + str(self.url)

        return url

    def get_picture(self):
        if not self.image:
            no_picture = '/static/img/user.png'
            return no_picture

        return self.image.url

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username