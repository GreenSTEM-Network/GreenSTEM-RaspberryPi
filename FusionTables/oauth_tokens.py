#!/usr/bin/python
#
# Copyright (C) 2011 Google Inc.

""" Fusion Tables OAuth Helper

Retrieve OAuth 2.0 access and refresh tokens for Fusion Tables.
"""

import urllib2, urllib, json
client_id = ""
client_secret = ""
redirect_uri = "http://localhost"

def retrieve_tokens(client_id, client_secret, redirect_uri):

  print
  print 'Visit the URL below in a browser to authorize'
  print
  print '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code' % \
    ('https://accounts.google.com/o/oauth2/auth', 
    client_id,
    redirect_uri,
    'https://www.googleapis.com/auth/fusiontables')
  print
  
  auth_code = raw_input('Enter authorization code ("code" parameter of URL): ')

  data = urllib.urlencode({
    'code': auth_code, 
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
  })
  request = urllib2.Request(
    url='https://accounts.google.com/o/oauth2/token',
    data=data)
  request_open = urllib2.urlopen(request)
  
  response = request_open.read()
  tokens = json.loads(response)
  access_token = tokens['access_token']
  refresh_token = tokens['refresh_token']
  return access_token, refresh_token


if __name__ == "__main__":
  import sys

  if len(sys.argv) == 4:
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    redirect_uri = sys.argv[3]

  access_token, refresh_token = retrieve_tokens(client_id,
                                                client_secret,
                                                redirect_uri)
  print
  print "Access Token: %s" % (access_token)
  print "Refresh Token: %s" % (refresh_token)
  print

  data = urllib.urlencode({
  'client_id': '',
  'client_secret': '',
  'refresh_token': refresh_token,
  'grant_type': 'refresh_token'})
  request = urllib2.Request(
  url='https://accounts.google.com/o/oauth2/token',
  data=data)

  table_id = ''

  query = "INSERT INTO %s(EXAMPLE_COL1,EXAMPLE_COL2) VALUES"\
        "('EXAMPLE_INFO1','EXAMPLE_INFO2')" % table_id # Single quotes
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  request = urllib2.Request('https://www.google.com/fusiontables/api/query?%s' % \
    (urllib.urlencode({'access_token': access_token,
                       'sql': query})),
    headers={'Content-Length':0})      # Manually set length to avoid 411 error
  request.get_method = lambda: 'POST'    # Change HTTP request method
  response = opener.open(request).read()
  print response
