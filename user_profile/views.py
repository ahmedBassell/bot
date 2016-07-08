from django.shortcuts import render

from django.shortcuts 			import render_to_response
from django.views.generic.base 	import TemplateView
from django.http 				import HttpResponse
from django.http 				import JsonResponse
from django.template.loader 	import get_template
from django.template 			import Context

from django.core import serializers

import json
# models
from django.contrib.auth.models import User
from models import *

# Create your views here.
def get_emotions_score(request):
	if(not request.user.is_authenticated()):
		return JsonResponse({'response':'forbidden'})


	user_profile = UserProfile.objects.get(user = request.user)
	# user_profile = UserProfile.objects.all()

	# user_profile = json.dumps(user_profile)
	user_profile = toJson(user_profile)
	
	return HttpResponse(user_profile, content_type='application/json')





def toJson(var):
	data = serializers.serialize("json", [var])
	struct = json.loads(data)
	result = []
	for i in struct:
		result.append(i['fields'])
	result = json.dumps(result)
	return result