from gambitChallenge.celery import app as celery_app
from .dataProcessing import modbusDataEntryAutomate

@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(300.0, newTest.s(), name='modbusDataEntryAutomate activated :)')

@celery_app.task
def test(arg):
	print arg

@celery_app.task
def newTest():
	modbusDataEntryAutomate()
	return

# NOTE: http://stackoverflow.com/questions/41119053/connect-new-celery-periodic-task-in-django