from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from main.models import ToDoList
from .forms import CreateNewList, CreateNewTask


# Create your views here.
def view_todos(response, id):
	ls = ToDoList.objects.get(id=id)
	items = ls.item_set.all()

	if response.method == 'POST':
		print(response.POST)
		if response.POST.get('save'):
			for item in ls.item_set.all():
				if response.POST.get(f"c{str(item.id)}") == 'clicked':
					item.complete = True
				else:
					item.complete = False
				item.save()
		# DONE Added way to delete lists
		elif response.POST.get('delete-list'):
			return HttpResponseRedirect(f'/{id}/delete')
		elif response.POST.get('new-item'):
			return HttpResponseRedirect(f'{id}/create-task')
	return render(response, 'main/todolist.html', {'todo_name': ls, 'items': items, 'id': id})


def confirm_list_delete(response, id):
	# DONE Made user confirm if they *really* want to delete a list
	ls = ToDoList.objects.get(id=id)

	if response.method == 'POST':
		if response.POST.get('really-delete'):
			ls.delete()
			return HttpResponseRedirect('/')
		elif response.POST.get('dont-delete'):
			return HttpResponseRedirect(f'/{id}')
	return render(response, 'main/confirm-list-delete.html', {'todo_name': ls, 'id': id})


def index(response):
	# Print out links to each list in database.
	# Each link redirects to appropriate lists.
	# DONE Find way to get the id of each list.
	tdls = ToDoList.objects.all()
	return render(response, 'main/home.html', {'todolists': tdls, 'id': 1})


def create_list(response):

	if response.method == 'POST':
		form = CreateNewList(response.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			t = ToDoList(name=name)
			t.save()

		return HttpResponseRedirect(f"/{t.id}")
	else:
		form = CreateNewList()
	form = CreateNewList()
	return render(response, 'main/create-list.html', {'form': form})


def create_task(response, id):
	form = CreateNewTask()
	if response.method == 'POST':
		form = CreateNewTask(response.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			complete = form.cleaned_data['completed']
			print(name)
			print(complete)
			t = ToDoList.objects.get(id=id)
			t.item_set.create(text=name, complete=complete)
			t.save()
			return HttpResponseRedirect(f"/{t.id}")
		else:
			form = CreateNewTask()
	return render(response, 'main/create-task.html', {'form': form, 'id': id})


# TODO View details on individual items.
def view_item(response, list_id, item_id):
	todo_item = ToDoList.objects.get(id=list_id).item_set.get(id=item_id)
	return render(response, 'main/item.html', {'todo': todo_item})
