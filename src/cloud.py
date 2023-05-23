
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools


class Cloud:

  # define path variables
  credentials_file_path =  '/opt/surveillance/credentials/credentials.json'
  clientsecret_file_path = '/opt/surveillance/credentials/surveillance_client.json'

  # define API scope
  SCOPE = 'https://www.googleapis.com/auth/drive'

  def __init__(self):  
    # define store
    store = file.Storage(self.credentials_file_path)
    credentials = store.get()
    # get access token
    if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(self.clientsecret_file_path, self.SCOPE)
      credentials = tools.run_flow(flow, store)
    # define API service
    http = credentials.authorize(Http())
    self.drive = discovery.build('drive', 'v3', http=http)

  # define a function to retrieve all files
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

    except errors.HttpError as error:
      print(f'An error has occurred: {error}')
    #    break
    # output the file metadata to console
    for oneFile in results:
      print(oneFile)


if __name__ == '__main__':
  myCloud = Cloud()
  myCloud.retrieve_all_files(myCloud.drive)
  exit()        
