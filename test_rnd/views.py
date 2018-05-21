import subprocess
import os
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from django.http import HttpResponse
from django.shortcuts import render
from subprocess import Popen, PIPE

from .forms import ChatForm
# import rasa
# import rasa_core

def index(request):
	#command = 'python -m rasa_core.run -d rasa/models/dialogue -u rasa/models/nlu/default/current'
	#result = subprocess.run(command, shell=True)
	# #output = result.stdout.decode("utf-8")
	# #output = "\n".join(output.splitlines())
	# output=''
	# for line in result.stdout:
	# 	print(line.decode(), end='')
	return render(request, 'bot_ui/index.html')

def get_input(request):
	if request.method == 'POST':
		form = ChatForm(request.POST)
		if form.is_valid():
			user_input = request.POST.get('input_text')
			all_inputs = chatLogger(user_input)
			
			# html_ = '''<div class="chat-message clearfix">
			# 			<div class="chat-message-content clearfix">	<span class="chat-time">13:37</span>
			# 				<h5> You </h5>
			# 				<p> ''' + user_input +''' </p>
			# 			</div>
			# 			<!-- end chat-message-content -->
			# 		</div>'''
			return render(request, 'bot_ui/index.html', {'all_inputs':all_inputs})
	else:
		form = ChatForm()

	return render(request, 'bot_ui/index.html', {'form':form})

def chatLogger(input):
	chat_history = []
	chat_history.append(input)
	return chat_history


def train(request):
	from rasa_nlu.converters import load_data
	from rasa_nlu.config import RasaNLUConfig
	from rasa_nlu.model import Trainer

	training_data = load_data('data/demo_rasa.json')
	trainer = Trainer(RasaNLUConfig("nlu_model_config.json"))
	trainer.train(training_data)
	model_directory = trainer.persist('models/nlu/', fixed_model_name="current")

	from rasa_nlu.model import Metadata, Interpreter
	interpreter = Interpreter.load(train_nlu())
	json = interpreter.parse("hello")
	print(json)
	return HttpResponse(json)