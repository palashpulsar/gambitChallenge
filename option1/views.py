from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import modbusDataTable

from dataProcessing import readDataFromURL, variableNames, convert2HumanData2
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.db import IntegrityError
import json


# Create your views here.
def dataConversion(request):
	# modelData = modbusDataTable.objects.all()[2]
	modelData = modbusDataTable.objects.latest('datetimestamp')
	print "Human Data: \n", type(modelData.humanData)
	print "Machine Data: \n", type(json.loads(modelData.machineData))
	print "Date stamp: \n", type(modelData.datetimestamp)
	if request.is_ajax():
		print "AJAX activated."
		humanData = json.loads(modelData.humanData)
		machineData = json.loads(modelData.machineData)
		datetimestamp = modelData.datetimestamp
		print humanData
		return JsonResponse(humanData, safe=False)
	return render(request, 'option1/interface.html')

def test(request):
	modelData = modbusDataTable.objects.latest('datetimestamp')
	data = json.loads(modelData.machineData)
	print data
	return JsonResponse(data, safe=False)


def rearrangeDatabase():
	print "I am inside rearrangeDatabase"
	allEntry = modbusDataTable.objects.all().order_by('datetimestamp')
	obj = allEntry[0]
	for i in range(len(allEntry)-1):
		machineData = json.loads(allEntry[i].machineData)
		machineData = dict([(int(k), v) for k, v in machineData.items()])
		dictVar = variableNames()
		humanData = convert2HumanData2(machineData, dictVar)
		allEntry[i].humanData = json.dumps(humanData)
		allEntry[i].save()
	return