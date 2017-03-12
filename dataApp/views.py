from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import modbusDataTable
import json


# Create your views here.

"""
Description:
	The following function extracts the content of latest entry into database.
"""
def latestDataEntry(request):
	modelData = modbusDataTable.objects.latest('datetimestamp')
	humanData = json.loads(modelData.humanData)
	machineData = json.loads(modelData.machineData)
	datetimestamp = modelData.datetimestamp
	return JsonResponse(humanData, safe=False)

"""
Description of retrieveVariableList:
	The following function returns the variable lists to frontend.
"""
def retriveVariableList(request):
	varList = [];
	modelData = modbusDataTable.objects.latest('datetimestamp')
	for key in json.loads(modelData.humanData):
		varList.append(key)
	return JsonResponse(varList, safe=False)

"""
Description of retrieveData:
	The following function retrieves the required data from database and send it to front end.
	The function receives the type of data (Register/Modbus data or Human readable data),
	and the name of the variable (either Register number or Human-Names variable) from the
	frontend using GET.
	The function extracts the required data from database, and send it to frontend
	NOTE: For limited number of data, I am sending the data from the last 5 (numElement) entries
"""
def retrieveData(request):
	varType = request.GET['varType']
	varName = request.GET['varName']
	numElement = 5

	# Selecting the objects
	allEntry = modbusDataTable.objects.all().order_by('-datetimestamp')[:numElement]
	allEntry = reversed(allEntry)

	# Assigning the values corresponding to reg_id and their datetimestamp in a variable
	dataDateTimeStamp = []
	dataVarName = []
	for obj in allEntry:
		dataDateTimeStamp.append(obj.datetimestamp)
		if varType == 'modbus':
			objDict = json.loads(obj.machineData)
			dataVarName.append(objDict[varName])
		elif varType == 'human':
			objDict = json.loads(obj.humanData)
			dataVarName.append(objDict[varName]["human"])
	allData = {'datetimestamp': dataDateTimeStamp, 'dataVar': dataVarName}
	return JsonResponse(allData, safe=False)