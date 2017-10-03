#!/usr/bin/python

import httplib2

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
import json


# Copy your credentials from the console
CLIENT_ID = '726229043774-tndi227mdnltqsiab1hu96lp48bv24p0.apps.googleusercontent.com'
CLIENT_SECRET = 'ABk2IwJC8SXltuW3u7ou8sJ-'

# Check https://developers.google.com/webmaster-tools/search-console-api-original/v3/ for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print('Go to the following link in your browser: ' + authorize_url)
code = input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

webmasters_service = build('webmasters', 'v3', http=http)

# Retrieve list of properties in account
site_list = webmasters_service.sites().list().execute()

# Filter for verified websites
verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                       if s['permissionLevel'] != 'siteUnverifiedUser'
                          and s['siteUrl'][:4] == 'http']

site = verified_sites_urls[0]
print(type(site))

with open("C:/Users/User/Documents/tom/automation/consoleAPI/outs/crawlErrors.json") as outfile:
    for site_url in verified_sites_urls:
        print("Getting Errors for " + site_url + "...")
        crawl_error = webmasters_service.urlcrawlerrorscounts().query(siteUrl = site_url).execute()
        json.dump(crawl_error, outfile)
        print(crawl_error)
