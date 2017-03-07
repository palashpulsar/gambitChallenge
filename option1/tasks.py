# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .views import readDataFromURL

logger = get_task_logger(__name__)

# @periodic_task(
# 	run_every=(crontab()),
# 	name="testingPeriodicTask",
# 	ignore_result=True
# )
def testingPeriodicTask():
	readDataFromURL("http://tuftuf.gambitlabs.fi/feed.txt")
	logger.info("testingPeriodicTask is now activated")


@shared_task
def add(x, y):
	return x + y


@shared_task
def mul(x, y):
	return x * y


@shared_task
def xsum(numbers):
	return sum(numbers)

def readDataFromURL(targetURL):
	"""
	Description:
	This function reads the text obtained from 'targetURL'.
	It parses the text into individual register reading, date as well as time.
	It returns a dictionary with keys as register number, and values as the corresponding value.
	The dictionary also includes the date and time.
	
	Input:
	targetURL: The url string from where text file is generated.
	
	Output:
	machineData: A dictionary that comprises the content of registers, as well as date and time.
	"""
	txt = urllib2.urlopen(targetURL)
	machineData = {}
	for line in txt:
		if '-' in line: # That is, this is the date and time field
			machineData['date'] = line.split(' ')[0]
			machineData['time'] = line.split(' ')[1].split('\n')[0]
		else:
			machineData[int(line.split(':')[0])] = int(line.split(':')[1])
	print "modbus data:\n", machineData
	return machineData