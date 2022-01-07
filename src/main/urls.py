# from django.shortcuts import render
from django.urls import path
from . import views


urlpatterns = [
	path('', views.index),
	path('<int:id>', views.view_todos),
	path('<int:list_id>/item/<int:item_id>', views.view_item),
	path('<int:id>/delete', views.confirm_list_delete),
	path('create-list/', views.create_list),
	path('<int:id>/create-task/', views.create_task)
]
