from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from .models import *
from multi_email_field.forms import MultiEmailField

class CustomerForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['readonly'] = True

	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class leaveform(forms.Form):

	def __init__(self, user, *args, **kwargs):
		super(leaveform, self).__init__(*args, **kwargs)
		self.fields['subject'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in leave_choice.objects.filter()]
        )
		self.fields['content'] = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

	# from_email = forms.EmailField()
	to_email = forms.EmailField()
	cc = forms.EmailField()


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser']

