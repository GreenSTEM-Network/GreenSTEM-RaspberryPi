import urllib2
import urllib
import simplejson
import sys
import httplib

data = urllib.urlencode({
    'client_id': '',
    'client_secret': '',
    'refresh_token': 'refresh_token',
    'grant_type': 'refresh_token'})
request = urllib2.Request(
    url='https://accounts.google.com/o/oauth2/token',
    data=data)
request_open = urllib2.urlopen(request)
response = request_open.read()
request_open.close()
tokens = json.loads(response)
access_token = tokens['access_token']

table_id = ''

query = "INSERT INTO %s(EXAMPLE_COL1,EXAMPLE_COL2) VALUES"\
        "('EXAMPLE_INFO1','EXAMPLE_INFO2')" % table_id  # Single quotes
opener = urllib2.build_opener(urllib2.HTTPHandler)
request = urllib2.Request('https://www.google.com/fusiontables/api/query?%s' %
                          (urllib.urlencode({'access_token': access_token,
                                             'sql': query})),
                          headers={'Content-Length': 0})      # Manually set length to avoid 411 error
request.get_method = lambda: 'POST'    # Change HTTP request method
response = opener.open(request).read()
print response
