from django.shortcuts import render

from django.shortcuts 			import render_to_response
from django.views.generic.base 	import TemplateView
from django.http 				import HttpResponse
from django.http 				import JsonResponse
from django.template.loader 	import get_template
from django.template 			import Context
import os
from django.conf import settings


# rest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# remove csrf
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.

from op import operations
from py27.chatbot import bot

from django.utils import timezone

from django.core import serializers
from django.db.models import Q

# MODELS
from django.contrib.auth.models import User
from models import Conversation

sara = bot('Sara')
@csrf_exempt # remove csrf
# @api_view(['GET', 'POST'])
def result(request):
	if(not request.user.is_authenticated()):
		return JsonResponse({'response':'forbidden'})
	res = {}
	if request.method == 'POST':
		received_json_data=json.loads(request.body)
		user_input = received_json_data['input']
		
		datetime = timezone.now()
		bot = User.objects.get(username="bot")
		c = Conversation(text=user_input, date=datetime, sender_id=request.user, receiver_id=bot)
		c.save()


		sara.set_input(user_input)
        sara.validate_input()
        sara.preprocess_input()
        
        output = sara.print_response()

        reply = Conversation(text=output, date=datetime, sender_id=bot, receiver_id=request.user)
        reply.save()
        

        res = {
        	'input': user_input,
        	'output': output
        }
        # res = json.dumps(res)
        # json.dumps(json.JSONDecoder().decode(res))
        # res = serializers.serialize('json', res)
	return JsonResponse(res, safe=False)


@csrf_exempt
def chats(request):
	if(not request.user.is_authenticated()):
		return JsonResponse({'response':'forbidden'})
	users = User.objects.all()
	
	convs = Conversation.objects.filter( Q(sender_id   =  request.user) | Q(receiver_id = request.user) ).order_by('date')
	

	data = serializers.serialize("json", convs)
	struct = json.loads(data)
	result = []
	for i in struct:
		result.append(i['fields'])
	data = json.dumps(result)
	return HttpResponse(data, content_type='application/json')
	# return JsonResponse(data, safe=False)
