from django import forms


class CreateNewList(forms.Form):
	name = forms.CharField(label='List Name: ', max_length=200)


class CreateNewTask(forms.Form):
	name = forms.CharField(label='Task Name', max_length=300)
	completed = forms.BooleanField(required=False, label='Completed')
	description = forms.CharField(required=False, max_length=500)
