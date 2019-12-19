#!/usr/bin/env python

import collections
import json
import requests

from mddns import settings

class ZoneWrap(object):

	def __init__(self, jsondict):
		zone = self.constructTuple('Zone', jsondict)
		self.zone = zone._replace(
					rrsets=[self._rrset(rrdata) for rrdata in zone.rrsets]
				)

	def constructTuple(self, name, jsondict):
		return collections.namedtuple(name, jsondict.keys())(*jsondict.values())


	def deconstructTuple(self, tpl, **kwlistmaps):
		d = dict(tpl._asdict())
		for k, f in kwlistmaps.items():
			d[k] = list(map(f, d[k]))
		return d

	def _rrset(self, rrdata):
		rrdata["records"] = [self.constructTuple('Record', rdata) for rdata in rrdata["records"]]
		return self.constructTuple('RRSet', rrdata)

	def asdict(self):
		return self.deconstructTuple(self.zone,
				rrsets=lambda rs: self.deconstructTuple(rs,
				records=lambda rc: self.deconstructTuple(rc)))


class PowerDNS(object):

	basepath = "api/v1"

	def __init__(self, server, apikey, server_id='localhost'):
		self.server = server
		self.apikey = apikey
		self.server_id = server_id

	def join(self, *fields):
		return "/".join(fields)

	def _url(self, url):
		return self.join(self.server, self.basepath, url)

	def _zoneurl(self, *urls):
		return self.join("servers", self.server_id, "zones", *urls)

	def _headers(self, **additional_headers):
		additional_headers.update({'X-Api-Key': self.apikey})
		return additional_headers

	def _get(self, url):
		return requests.get(self._url(url),
				headers=self._headers())

	def _post(self, url, jsondict):
		return requests.post(self._url(url),
				headers=self._headers(),
				json=jsondict)

	def _patch(self, url, jsondict):
		return requests.patch(self._url(url),
				headers=self._headers(),
				json=jsondict)

	def _zone_get(self, *urls):
		return self._get(self._zoneurl(*urls))

	def zones(self):
		return [zone["name"] for zone in self._zone_get().json()]

	def zone(self, zone_id):
		return ZoneWrap(self._zone_get(zone_id).json())

	def delete_record(self, zone_id, name, type):
		payload = {"rrsets": [dict(
					name=".".join([name, zone_id]),
					type=type,
					changetype="DELETE")]}

		return self._patch(self._zoneurl(zone_id), payload)

	def set_record(self, zone_id, name, ttl, type, content):
		payload = {"rrsets": [dict(
					name=".".join([name, zone_id]),
					ttl=ttl,
					type=type,
					changetype="REPLACE",
					records=[dict(
							content=content,
							disabled=False,
						)])]}

		return self._patch(self._zoneurl(zone_id), payload)


pdns = PowerDNS(settings.POWERDNS_URL, settings.POWERDNS_KEY)
