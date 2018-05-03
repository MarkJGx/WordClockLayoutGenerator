#!/usr/bin/python


from __future__ import print_function
import argparse
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# usage ./generate_layout.py "sheet_id" "range_name"
parser = argparse.ArgumentParser()
parser.add_argument('spreadsheet_id', type=str)
parser.add_argument('range_name', type=str)


args = parser.parse_args()

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))
RANGE_NAME = 'Sheet4!A1:C'
result = service.spreadsheets().values().get(spreadsheetId=args.spreadsheet_id,
                                             range=args.range_name).execute()
# converts Google Sheet data into a dict
values = result.get('values', [])
if not values:
    print('No data found.')
else:
    print('Variable Names, Row, Column Range:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        # Rows and Columns start at 1 in Sheets
        print('%s, %s, %s' % (row[0], row[1], row[2]))
