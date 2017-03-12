from gambitChallenge.celery import app as celery_app
from .dataProcessing import modbusDataEntryAutomate

@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(300.0, newTest.s(), name='modbusDataEntryAutomate activated :)')


"""
The following task is for performing every 5 minutes.
It saves new data from live feed into the database.
"""
@celery_app.task
def newTest():
	modbusDataEntryAutomate()
	return

