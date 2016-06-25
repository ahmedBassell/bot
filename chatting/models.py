from __future__ import unicode_literals

from django.db import models


# import user
from django.contrib.auth.models import User
# Create your models here.

class Session(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sess')
	name = models.TextField()


class Conversation(models.Model):
	sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sen')
	receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rec')
	text = models.TextField()
	session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='sess')
	date = models.DateTimeField('date')

	def __unicode__(self):
		return unicode(self.text)

	def get_date(self):
		return unicode(self.date)

	def get_sender(self):
		return unicode(self.sender_id)
	
	def get_receiver(self):
		return unicode(self.receiver_id)