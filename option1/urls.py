from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^data/$', views.dataConversion, name='dataConversion'),
	url(r'^test/$', views.test, name='test'),
]