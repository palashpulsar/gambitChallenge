from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^varlist/', views.retriveVariableList, name='varliableList'),
	url(r'^retrieveData/', views.retrieveData, name='retrieveData'),
	url(r'^latestDataEntry/', views.latestDataEntry, name='latestDataEntry'),
]