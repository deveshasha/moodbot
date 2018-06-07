import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import ChatForm
from moodbot.settings import BASE_DIR

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

from rasa_core.agent import Agent

agent = Agent.load(os.path.join(BASE_DIR, 'rasa/models/dialogue') , interpreter = os.path.join(BASE_DIR, 'rasa/models/nlu/default/current'))

def index(request):
	return render(request, 'bot_ui/index.html')

def get_input(request):
	if request.method == 'POST':
		form = ChatForm(request.POST)
		print("##### inside post")
		#if form.is_valid():
		print("##### inside form valid")
		user_input = request.POST.get('user_input')
		bot_response = agent.handle_message(user_input)
		print("bot_response:" + bot_response[0])

		return JsonResponse({'user_input':user_input,'bot_response':bot_response})
			#return render(request, 'bot_ui/index.html', {'user_input':user_input,'bot_response':bot_response[0]})
	else:
		form = ChatForm()

	return render(request, 'bot_ui/index.html', {'form':form})

def rasa_train(request):
	training_data = load_data('rasa/data/demo_rasa.json')
	trainer = Trainer(RasaNLUConfig("rasa/nlu_model_config.json"))
	trainer.train(training_data)
	model_directory = trainer.persist('models/nlu/', fixed_model_name="current")
	interpreter = Interpreter.load(model_directory)
	intent_dict = interpreter.parse("hello")
	print(intent_dict['intent']['name'])
	return HttpResponse(intent_dict)

def rasa_core_run(request):
	agent = Agent.load('rasa/models/dialogue' , interpreter = '/rasa/models/nlu/default/current')
	bot_response = agent.handle_message('hello')
	print("bot_response" + bot_response[0])