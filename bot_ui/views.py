import subprocess
import os

from django.http import HttpResponse
from django.shortcuts import render

from subprocess import Popen, PIPE


def index(request):
	command = 'python -m rasa_core.run -d rasa/models/dialogue -u rasa/models/nlu/default/current'
	result = subprocess.run(command, shell=True)
	# #output = result.stdout.decode("utf-8")
	# #output = "\n".join(output.splitlines())
	# output=''
	for line in result.stdout:
		print(line.decode(), end='')
	return render(request, 'bot_ui/index.html')
