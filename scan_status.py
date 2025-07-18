# This program prints some basic information about your Tenable Vulnerability Management (TVM) scans. 
# It could be a starting point for alerting or just something to run to get a quick status check at the start of the day.

# This code is presented for example purposes and is unsupported.

import requests
import getpass
import json

# get API keys from user (this prevents secrets from ending up in command history or worse yet, being hardcoded)
accesskey = getpass.getpass(prompt='Enter your access key for TVM: ')
secretkey = getpass.getpass(prompt='Enter your secret key for TVM: ')

# make the API call to get scans list
url = "https://cloud.tenable.com/scans"
headers = {
    "accept": "application/json",
    "X-ApiKeys": "accessKey="+accesskey+";secretKey="+secretkey
  }
response = requests.get(url, headers=headers)

scans = json.loads(response.text)
for i in scans['scans']:
    details = url + '/'+i['schedule_uuid'] # get each scan's UUID
    response2 = requests.get(details, headers=headers) # get the details of the individual scan, which we can then parse and print
    scandetails = json.loads(response2.text)
    #You need some logic to look for the fields, as content varies. try/except is a crude way to do it but works if all you want is a scan name, status, and how many hosts it found, or for example purposes
    try:
        print(scandetails['info']['name'], scandetails['info']['status'], scandetails['info']['hostcount'], "host(s)")
    except:
        try:
            print(scandetails['info']['name'], scandetails['info']['status'])
        except:
            print(scandetails['info']['name'])
    #print(i) # this would just print all the raw JSON we got back from TVM - useful starting point if you want to refine the above
