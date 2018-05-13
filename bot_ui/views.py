from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'bot_ui/index.html')
	# template = loader.get_template('bot_ui/index.html')
	# return HttpResponse("Hello, world. You're at the polls index.")