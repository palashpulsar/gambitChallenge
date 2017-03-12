from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^visual/', views.visualization, name='visual'),
	url(r'^varlist/', views.retriveVariableList, name='varliableList'),
	url(r'^data/', views.retrieveData, name='data'),
]