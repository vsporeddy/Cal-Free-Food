#!/usr/bin/python

import httplib2
import gflags
import base64
import email
import re

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
from apiclient import errors
#from apiclient import discovery
#from discovery import build


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = './client_secret_119686003876-c78cm37js1r3lpnvascaqenrc87knifa.apps.googleusercontent.com.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
    credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

def get_msg(query, service = gmail_service, user_id = 'me'):
      try:
          response = service.users().messages().list(userId=user_id, q=query).execute()

          messages = []

          if 'messages' in response:
              messages.extend(response['messages'])

          while 'nextPageToken' in response:
              page_token = response['nextPageToken']
              response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
              messages.extend(response['messages'])

          return messages

      except errors.HttpError, error:
          print('An error occurred:' + error)



def run():
  food_msg = get_msg("food OR breakfast OR brunch OR lunch OR dinner OR drink OR pizza OR barbecue") #This will be reworked soon...
  for i in food_msg:
      message2 = gmail_service.users().messages().get(userId='me', id=i['id'], format='raw').execute()
      snip = message2['snippet']
      count = 0
      start, b = 0, False
      for c in snip:
          if c == "!" or c == "/" or c == "." or c == "?" or (c=="&" and b):
              snip=snip[start:count]
          if c == "&" and not b:
              start = count+6
              b=True
          count+=1

      #print snip

      snip += '.html'
      filename = 'templates/' + snip 
      filename2 = 'platter/' + snip

      message = gmail_service.users().messages().get(userId='me', id=i['id'], format='full').execute()
      if 'parts' in message['payload']:
          if message['payload']['parts'][0]['mimeType'] == 'multipart/alternative':
              message_raw = message['payload']['parts'][0]['parts'][0]['body']['data']    
          else:
            message_raw = message['payload']['parts'][0]['body']['data']   
      else:
          message_raw = message['payload']['body']['data']
      msg_str = base64.urlsafe_b64decode(message_raw.encode('ASCII'))

      
      msg = email.message_from_string(msg_str)
      f = open(filename, "w")
      g = open(filename2, "w")
      html = '{% extends "base.html" %}{% block title %} - Platter{% endblock %}{% block content %}<p><a href="{{ url_for("index") }}">home</a></p><pre>' + msg_str + '</pre>{% endblock %}'
      f.write(html)
      g.write(html)