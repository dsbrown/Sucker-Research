"""
Edmunds.com API Python wrapper
Edmunds API Documentation: http://developer.edmunds.com/

author: Michael Bock <mbock@edmunds.com>
version: 0.1.1
"""

import requests
from types import StringType, BooleanType

class Edmunds:
	"""
	The Edmunds API wrapper class
	"""
	
	BASE_URL = 'https://api.edmunds.com'
	BASE_MEDIA_URL = 'http://media.ed.edmunds-media.com'

	def __init__(self, key, debug=False):
		"""
		Constructor for Edmunds class

		:param key: Edmunds API key
		:param debug: True or False. If True, prints error messages
		:type key: str
		"""

		if not isinstance(debug, BooleanType):
			raise Exception('debug is not a BooleanType; class not instantiated')
		self._debug = debug

		if not isinstance(key, StringType):
			raise Exception('key not a StringType; class not instantiated')
		self._parameters = {'api_key' : key, 'fmt': 'json'}

	def make_call(self, endpoint, **kwargs):
		"""
		example calls:
		>>> make_call('/v1/api/vehiclephoto/service/findphotosbystyleid', comparator='simple', styleId='3883')
		>>> make_call('/api/vehicle/v2/lexus/rx350/2011/styles')

		Info about **kwargs: http://stackoverflow.com/questions/1769403/understanding-kwargs-in-python

		:param endpoint: Edmunds API endpoint, e.g. '/v1/api/vehiclephoto/service/findphotosbystyleid' or '/api/vehicle/v2/lexus/rx350/2011/styles'
		:type endpoint: str
		:param kwargs: List of extra parameters to be put into URL query string, e.g. view='full' or comparator='simple', styleId='3883'
		:type kwargs: List of key=value pairs, where the value is a str
		:returns: API response
		:rtype: JSON object
		"""
		# assemble url and queries
		payload = dict(self._parameters.items() + kwargs.items())
		url = self.BASE_URL + endpoint

		# make request
		try:
			r = requests.get(url, params=payload)
		# ConnectionError would result if an improper url is assembeled
		except requests.ConnectionError:
			if self._debug:
				print 'ConnectionError: URL was probably incorrect'
			return None
		except requests.Timeout:
			if self._debug:
				print 'Timeout Error'
			return None

		# extract JSON
		try:
			response_json = r.json()
		# ValueError would result if JSON cannot be parsed
		except ValueError:
			if self._debug:
				print 'ValueError: JSON could not be parsed'
				print 'Response:'
				print r.text
			return None

		return response_json
