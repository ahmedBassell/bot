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
from datetime import datetime

from django.core import serializers
from django.db.models import Q

# MODELS
from django.contrib.auth.models import User
from models import Conversation, Session
from user_profile.models import UserProfile


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
		session_id = received_json_data['session_id']
		
		session = Session.objects.get(id = session_id)

		dt = datetime.now() 
		bot = User.objects.get(username="bot")
		c = Conversation(text=user_input, date=dt, sender_id=request.user, receiver_id=bot, session_id = session)
		c.save()


		sara.set_input(user_input)
        sara.validate_input()
        sara.preprocess_input()
        
        output = sara.print_response()

        reply = Conversation(text=output, date=dt, sender_id=bot, receiver_id=request.user, session_id = session)
        reply.save()
        
        from emotion.emo.erf import Emotion
        emo = Emotion()
        result = emo.get_emotion(user_input)
        resultant_emo = get_max_emotion(result)

        user_profile = UserProfile.objects.get(user = request.user)
        if resultant_emo == "joy":
        	user_profile.joy_count = user_profile.joy_count + 1 
        elif resultant_emo == "sadness":
        	user_profile.sad_count = user_profile.sad_count + 1 
        elif resultant_emo == "anger":
        	user_profile.ang_count = user_profile.ang_count + 1 
        elif resultant_emo == "fear":
        	user_profile.fea_count = user_profile.fea_count + 1 
        elif resultant_emo == "disgust":
        	user_profile.dis_count = user_profile.dis_count + 1 

        user_profile.save()

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

	if request.method == 'GET':
		sess_id = request.GET.get('sess')
		sess = Session.objects.get(user_id = request.user, id = sess_id)
		if(sess == None):
			return JsonResponse({'response':'forbidden'})
		users = User.objects.all()
		
		convs = Conversation.objects.filter( (Q(sender_id   =  request.user) | Q(receiver_id = request.user)) & Q(session_id = sess_id)  ).order_by('date')
		

		data = serializers.serialize("json", convs)
		struct = json.loads(data)
		result = []
		for i in struct:
			result.append(i['fields'])
		data = json.dumps(result)

	return HttpResponse(data, content_type='application/json')
	# return JsonResponse({}, safe=False)


def get_max_emotion(result):
	import operator
	emo_dict = {'joy':0, 'sadness':0, 'disgust':0, 'anger':0, 'fear':0, 'shame':0}
	emo_dict[result['SVM']] = emo_dict[result['SVM']] + 1 
	emo_dict[result['Logistic Regression']]  = emo_dict[result['Logistic Regression']] + 1 
	emo_dict[result['Multinomial Naive Bayes']] = emo_dict[result['Multinomial Naive Bayes']] + 1
	return max(emo_dict.iteritems(), key=operator.itemgetter(1))[0]



