from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from option1.models import modbusDataTable
import json

# Create your views here.

def test(request):
	return render(request, 'option2/singlePage.html')

def visualization(request):
	print "Am I here?"
	return render(request, 'option2/visualization.html')

def varType_Modbus(request):
	varList = [];
	modelData = modbusDataTable.objects.latest('datetimestamp')
	for key in json.loads(modelData.machineData):
		varList.append(key)
	print varList
	return JsonResponse(varList, safe=False)

def varType_Human(request):
	varList = [];
	modelData = modbusDataTable.objects.latest('datetimestamp')
	for key in json.loads(modelData.humanData):
		varList.append(key)
	print varList
	return JsonResponse(varList, safe=False)


def callForModbusData(request):
	print "callForModbusData is selected."
	reg_id = request.GET['reg_id']
	numElement=5
	
	# Selecting the objects
	allEntry = modbusDataTable.objects.all().order_by('-datetimestamp')[:numElement]
	allEntry = reversed(allEntry)

	# Assigning the values corresponding to reg_id and their datetimestamp in a variable
	dataDateTimeStamp = []
	dataReg_id = []
	for obj in allEntry:
		objDict = json.loads(obj.machineData)
		dataDateTimeStamp.append(obj.datetimestamp)
		dataReg_id.append(objDict[str(reg_id)])
	allData = {'datetimestamp': dataDateTimeStamp, 'dataVar': dataReg_id}
	return JsonResponse(allData, safe=False)

def callForHumanData(request):
	print "callForHumanData is selected."
	humanVar = request.GET['humanVar']
	numElement = 5
	
	# Selecting the objects
	allEntry = modbusDataTable.objects.all().order_by('-datetimestamp')[:numElement]
	allEntry = reversed(allEntry)

	# Assigning the values corresponding to humanVar and their datetimestamp in a variable
	dataDateTimeStamp = []
	dataHumanVar = []
	for obj in allEntry:
		objDict = json.loads(obj.humanData)
		dataDateTimeStamp.append(obj.datetimestamp)
		dataHumanVar.append(objDict[humanVar]["human"])
	allData = {'datetimestamp': dataDateTimeStamp, 'dataVar': dataHumanVar}
	return JsonResponse(allData, safe=False)


