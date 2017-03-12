from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models

# Create your models here.
class modbusDataTable(models.Model):
	datetimestamp = models.DateTimeField(unique=True)
	machineData = JSONField()
	humanData = JSONField(null=True)
	def __unicode__(self):
		return unicode(self.datetimestamp)

