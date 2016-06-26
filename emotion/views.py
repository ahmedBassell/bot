from django.shortcuts import render

from django.shortcuts 			import render_to_response
from django.views.generic.base 	import TemplateView
from django.http 				import HttpResponse
from django.http 				import JsonResponse
from django.template.loader 	import get_template
from django.template 			import Context
import os
from django.conf import settings

# remove csrf
from django.views.decorators.csrf import csrf_exempt
import time
import json

# Models
# 
# Processing

# init
# Create your views here.
# global emo
@csrf_exempt # remove csrf
def find_emotion(request):

	if request.method == 'POST':
		# user_input = request.POST.get('input')
		received_json_data=json.loads(request.body)
		user_input = received_json_data['input']
		
		t0 = time.time()
		from emo.erf import Emotion
		emo = Emotion()
		result = emo.get_emotion(user_input)
		time_iter = (time.time() - t0)
		result['time']= time_iter
	else:
		# user_input = request.POST.get('input')
		# received_json_data=json.loads(request.body)
		# user_input = received_json_data['input']
		
		t0 = time.time()
		from emo.erf import Emotion
		emo = Emotion()
		result = emo.get_emotion('i feel happy')
		time_iter = (time.time() - t0)
		result['time']= time_iter
	return JsonResponse({'output': result}, safe=False)