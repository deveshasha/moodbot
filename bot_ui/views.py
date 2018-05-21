from django.http import HttpResponse
from django.shortcuts import render

from .forms import ChatForm

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

def index(request):
	return render(request, 'bot_ui/index.html')

def get_input(request):
	if request.method == 'POST':
		form = ChatForm(request.POST)
		if form.is_valid():
			user_input = request.POST.get('input_text')
			return render(request, 'bot_ui/index.html', {'user_input':user_input})
	else:
		form = ChatForm()

	return render(request, 'bot_ui/index.html', {'form':form})

def rasa_train(request):
	training_data = load_data('rasa/data/demo_rasa.json')
	trainer = Trainer(RasaNLUConfig("rasa/nlu_model_config.json"))
	trainer.train(training_data)
	model_directory = trainer.persist('models/nlu/', fixed_model_name="current")
	interpreter = Interpreter.load(model_directory)
	json = interpreter.parse("hello")
	print(json)
	return HttpResponse(json)