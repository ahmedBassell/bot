from __future__ import unicode_literals

from django.db import models


# import user
from django.contrib.auth.models import User
# Create your models here.

class Conversation(models.Model):
	sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sen')
	receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rec')
	text = models.TextField()
	date = models.DateTimeField('date')

	def __unicode__(self):
		return unicode(self.text)

	def get_date(self):
		return unicode(self.date)

	def get_sender(self):
		return unicode(self.sender_id)
	
	def get_receiver(self):
		return unicode(self.receiver_id)