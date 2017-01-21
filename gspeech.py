from googleapiclient import discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

def getservice():
    jsonname = 'try-apis-b81f9aa58144.json'
    scope = [ 'https://www.googleapis.com/auth/cloud-platform' ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonname, scope)
    print(str(credentials))
    http = credentials.authorize(httplib2.Http())

    service = discovery.build('speech','v1beta1',http=http)
    return service

if __name__=="__main__":
    print(getservice())