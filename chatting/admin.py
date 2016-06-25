from django.contrib import admin

# Register your models here.

from .models import Conversation, Session

admin.site.register(Conversation)
admin.site.register(Session)

# 