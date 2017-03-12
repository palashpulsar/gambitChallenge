from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^visual/', views.visualization, name='visual'),
	url(r'^machine', views.callForModbusData, name='modbus'),
	# url(r'^machine/(?P<reg_id>[0-9]+)', views.callForModbusData),
	url(r'^human/', views.callForHumanData, name='human'),
	url(r'^type/machine/', views.varType_Modbus, name='modbusType'),
	url(r'^type/human/', views.varType_Human, name='humanType'),
	url(r'^test/', views.test, name='test')
]