# Simple HTTP-Get-API

from django.http import HttpResponse
from django.shortcuts import render

from .models import *

import ipaddress

class MissingOrBrokenFields(Exception):
	pass


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def isOfIp(ip_s, klass):
	try:
		return str(klass(ip_s))
	except ipaddress.AddressValueError:
		return None


def testIP(key, querydict, klass, name):
	if key in querydict:
		res = isOfIp(querydict[key], klass)
		if res is None:
			raise MissingOrBrokenFields("No valid %s address" % name)
		return res


def read_params(request):
	querydict = request.GET
	
	if not "domain" in querydict:
		raise MissingOrBrokenFields("Missing domain for update")
	if not "key" in querydict:
		raise MissingOrBrokenFields("Missing key for update")

	name, zone = querydict["domain"].split(".", 1)
	if not zone.endswith("."):
		zone += "."
	key = querydict["key"]

	a    = testIP("a",    querydict, ipaddress.IPv4Address, "IPv4")
	aaaa = testIP("aaaa", querydict, ipaddress.IPv6Address, "IPv6")

	if a is None and aaaa is None:
		client_ip = get_client_ip(request)
		a = isOfIp(client_ip, ipaddress.IPv4Address)
		aaaa = isOfIp(client_ip, ipaddress.IPv6Address)

	return name, zone, key, a, aaaa


def validate_name_zone_key(name_s, zone_s, key):

	def fail():
		raise MissingOrBrokenFields("Wrong name/zone-combination or API key")

	try:
		zone = Zone.objects.get(zone=zone_s)
	except Zone.DoesNotExist:
		fail()

	try:
		name = RecordName.objects.get(zone=zone, name=name_s)
	except RecordName.DoesNotExist:
		fail()

	if name.apikey != key:
		fail()

	return name

def getRecord(name, type):
	try:
		return Record.objects.get(name=name, type=type.upper())
	except Record.DoesNotExist:
		return Record(name=name, type=type.upper())

def trySetRecord(name, type, data):
	if data is not None:
		rec = getRecord(name, type)
		rec.data = data
		rec.save()
		return True
	return False

def index(request):
	try:
		name, zone, key, a, aaaa = read_params(request)
		recordName = validate_name_zone_key(name, zone, key)

		trySetRecord(recordName, "A", a)
		trySetRecord(recordName, "AAAA", aaaa)
		
		return HttpResponse("Updated %s with %r/%r\n" % (recordName, a, aaaa))
	except MissingOrBrokenFields  as e:
		return HttpResponse(str(e), status=400)
	except BackendIntegrityError as e:
		return HttpResponse(str(e), status=502)



