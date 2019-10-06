from django.contrib.auth.models import User
from django.db import models


class Zone(models.Model):
	zone = models.CharField(max_length=128, unique=True)


class RecordName(models.Model):
	name = models.CharField(max_length=128)
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

	apikey = models.CharField(max_length=128)

	owners = models.ManyToManyField(User, related_name="recordnames")

	class Meta:
		unique_together = (("name", "zone"), )


class Record(models.Model):
	rname  = models.ForeignKey(RecordName, 
		related_name="records",
		on_delete=models.CASCADE)

	rclass = models.CharField(max_length=2)
	rtype  = models.CharField(max_length=16)
	rttl   = models.PositiveIntegerField(default=300)
	rdata  = models.CharField(max_length=128)

