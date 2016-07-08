from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):  
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    joy_count = models.IntegerField(default = 1)
    sad_count = models.IntegerField(default = 1)
    ang_count = models.IntegerField(default = 1)
    fea_count = models.IntegerField(default = 1)
    dis_count = models.IntegerField(default = 1)
    

    def __unicode__(self):
        return unicode(self.user)
