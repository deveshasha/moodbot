from django import forms

class ChatForm(forms.Form):
	input_text = forms.CharField(max_length=100)
