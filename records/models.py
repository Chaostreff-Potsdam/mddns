from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from pypodonasy import pypodonasy

import random
import string

class BackendIntegrityError(IntegrityError):

	def __init__(self, response=None, exception=None):
		super(BackendIntegrityError, self).__init__("Could not write changes to PowerDNS backend.")
		self.response = response
		self.exception = None


class Zone(models.Model):
	zone = models.CharField(max_length=128, unique=True)

	allowed_users = models.ManyToManyField(User, related_name="zones")

	def __str__(self):
		return self.zone


def generate_api_key(keylen=32):
	available_chars = string.ascii_letters + string.digits
	return "".join(random.choice(available_chars) for _ in range(keylen))



class RecordName(models.Model):
	validhostname = RegexValidator(r'^([A-Za-z0-9\_]|[A-Za-z0-9\_][A-Za-z0-9\_\-]*[A-Za-z0-9])$',
			'Names may not start or end with - and may only include alphanums and -.')
	

	name = models.CharField(max_length=128, validators=[validhostname])
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

	apikey = models.CharField(max_length=128, default=generate_api_key)

	description = models.TextField(max_length=256, blank=True)

	owners = models.ManyToManyField(User, related_name="recordnames", help_text='You will be added automatically on save.')

	class Meta:
		unique_together = (("name", "zone"), )
		verbose_name = "Hostname"
		verbose_name_plural = "Hostnames"

	def fullname(self):
		return ".".join((self.name, self.zone.zone))

	def __str__(self):
		return self.fullname()


class Record(models.Model):
	A_RECORD = "A"
	AAAA_RECORD = "AAAA"

	SUPPORTED_TYPES = [
			(A_RECORD, "A"),
			(AAAA_RECORD, "AAAA"),
		]

	name  = models.ForeignKey(RecordName,
		related_name="records",
		on_delete=models.CASCADE)

	type  = models.CharField(
				max_length=16,
				choices=SUPPORTED_TYPES,
				default=A_RECORD
			)
	ttl   = models.PositiveIntegerField(default=300)
	data  = models.CharField(max_length=128)

	class Meta:
		unique_together = (("name", "type"), )

	def __str__(self):
		return "Record(%s, %s, %s)" % (self.name, self.type, self.data)

	def save(self, *args, **kwargs):
		try:
			resp = pypodonasy.pdns.set_record(self.name.zone.zone, self.name.name, self.ttl, self.type, self.data)
		except Exception as e:
			raise BackendIntegrityError(exception=e)
		if resp.status_code != 204:
			raise BackendIntegrityError(resp)
		super().save(*args, **kwargs)

	def pre_delete(self):
		try:
			resp = pypodonasy.pdns.delete_record(self.name.zone.zone, self.name.name, self.type)
		except Exception as e:
			raise BackendIntegrityError(exception=e)
		if resp.status_code != 204:
			raise BackendIntegrityError(resp)

from django.db.models import signals
from django.dispatch import receiver

@receiver(signals.pre_delete, sender=Record)
def delete_Record(sender, instance, using, *args, **kwargs):
	instance.pre_delete()

