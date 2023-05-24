
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from urllib.error import HTTPError
from googleapiclient.errors import HttpError
import survprop

class Cloud:

  # define path variables
  # credentials_file_path =  '/opt/surveillance/credentials/credentials.json'
  # clientsecret_file_path = '/opt/surveillance/credentials/surveillance_client.json'
  credentials_file_path =  None
  clientsecret_file_path = None

  # define API scope
  SCOPE = 'https://www.googleapis.com/auth/drive'

  def __init__(self, props):  
    # define store
    self.credentials_file_path = props.credentials_file
    self.clientsecret_file_path = props.client_secret_file
    store = file.Storage(self.credentials_file_path)
    credentials = store.get()
    # get access token
    if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(self.clientsecret_file_path, self.SCOPE)
      credentials = tools.run_flow(flow, store)
    # define API service
    http = credentials.authorize(Http())
    self.drive = discovery.build('drive', 'v3', http=http)
    self.topLevelDir = None

  # TEST: define a function to retrieve all files
  def retrieve_all_files(self,api_service):
    results = []
    page_token = None

    # while True:
    try:
      param = {}

      if page_token: param['pageToken'] = page_token

      files = api_service.files().list(**param).execute()
      # append the files from the current result page to our list
      results.extend(files.get('files'))
      # Google Drive API shows our files in multiple pages when the number of files exceed 100
      page_token = files.get('nextPageToken')

      #if not page_token:
      #    break

    except HttpError as error:
      print(f'An error has occurred: {error}')
    #    break
    # output the file metadata to console
    for oneFile in results:
      print(oneFile)

  def dir_exists(self, api_service, name):
    results = []
    try:
      param = {}
      param['q'] = 'name=\'' + name + '\''
      # param['q'] = 'parents = [] and name=\'' + name + '\''
      param['fields'] = '*'

      files = api_service.files().list(**param).execute()
      # append the files from the current result page to our list
      results.extend(files.get('files'))

    except HttpError as error:
      print(f'An error has occurred: {error}')
    # output the file metadata to console
    for oneFile in results:
      # print(oneFile)
      par = oneFile.get('parents')
      if not par:
          # print('This is it')
          self.topLevelDir = oneFile
      # print(oneFile.get('parents'))
      


if __name__ == '__main__':
  myProps = survprop.SurvProp()
  myCloud = Cloud(myProps)
  myCloud.dir_exists(myCloud.drive, '2023')
  print(myCloud.topLevelDir)
  exit()        
