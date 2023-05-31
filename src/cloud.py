
from apiclient import discovery
from httplib2 import Http
# from oauth2client import client, file, tools
from google.oauth2 import service_account
from googleapiclient.discovery import build
from urllib.error import HTTPError
from googleapiclient.errors import HttpError
import survprop

class Cloud:

  # define path variables
  credentials_file_path =  None
  clientsecret_file_path = None
  toplevel_dir = None
  # define API scope
  SCOPES = ['https://www.googleapis.com/auth/drive']
  # domain = 'gmail.com'
  # user = 'lars.vatne' # id only (ie. without @domain)


  def __init__(self, props):  
    # define store
    self.credentials_file_path = props.credentials_file
    # self.clientsecret_file_path = props.client_secret_file
    # store = file.Storage(self.credentials_file_path)
    # credentials = store.get()
    # subject = ''.join([self.user,'@',self.domain]);
    credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path, scopes=self.SCOPES)
    # get access token
    #if not credentials or credentials.invalid:
    #  flow = client.flow_from_clientsecrets(self.clientsecret_file_path, self.SCOPE)
    #  credentials = tools.run_flow(flow, store)
    # define API service
    # http = credentials.authorize(Http())
    # self.drive = discovery.build('drive', 'v3', http=http)
    self.drive = build('drive', 'v3', credentials=credentials)
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


  # Check if a certain directory exists below a specified parent
  # Return the ID if exists, Or None
  
  def dir_exists(self, api_service, parent_id, name):
    return_id = None
    results = []
    try:
      param = {}
      param['q'] = 'name=\'' + name + '\' and \'' + parent_id + '\' in parents and mimeType=\'application/vnd.google-apps.folder\''

      files = api_service.files().list(**param).execute()
      # append the files from the current result page to our list
      results.extend(files.get('files'))

    except HttpError as error:
      print(f'An error has occurred: {error}')
    # output the file metadata to console
    for oneFile in results:
      return_id = oneFile['id']
      print(oneFile)
    return return_id

  # Create a folder inside a specified folder.
  # Return the ID of the newly created folder.
  
  def create_dir(self, api_service, parent_id, name):
    return_id = None
    results = []
    try:
      file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
      }

      file = api_service.files().create(body=file_metadata, fields='id').execute()
      print(F'Folder ID: "{file.get("id")}".')
      return_id = file.get('id')
      self.share_file(return_id)
    except HttpError as error:
      print(f'An error has occurred: {error}')
    return return_id
    
  def create_toplevel_dir(self, api_service, parent_id, name):
    return_id = None
    results = []
    try:
      file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
      }

      file = api_service.files().create(body=file_metadata, fields='id').execute()
      print(F'Folder ID: "{file.get("id")}".')
      return_id = file.get('id')
    except HttpError as error:
      print(f'An error has occurred: {error}')
    return return_id
      

  def check_dir(self, api_service, file_id):
    results = []
    try:
      param = {}
      param['fileId'] = file_id
      # param['q'] = 'parents = [] and name=\'' + name + '\''
      # param['fields'] = 'files(id, name)'

      chk_file = api_service.files().get(**param).execute()
      # append the files from the current result page to our list
      # results.extend(files.get('files'))

    except HttpError as error:
      print(f'An error has occurred: {error}')
    # output the file metadata to console
    return chk_file['id']

  def share_file(self, file_id):
    permission1 = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': 'lars.vatne@gmail.com',  # Please set your email of Google account.
    }
    self.drive.permissions().create(fileId=file_id, body=permission1).execute()

if __name__ == '__main__':
  myProps = survprop.SurvProp()
  myCloud = Cloud(myProps)
  # permission1 = {
  #        'type': 'user',
  #        'role': 'writer',
  #        'emailAddress': 'lars.vatne@gmail.com',  # Please set your email of Google account.
  #     }
  # myCloud.drive.permissions().create(fileId=myProps.toplevel_folder_id, body=permission1).execute()

  
  #topDir = myCloud.create_toplevel_dir(myCloud.drive, 'ABC', 'surveillance')
  #print(topDir)
  # myCloud.retrieve_all_files(myCloud.drive)
  surv_dir = myCloud.check_dir(myCloud.drive, myProps.toplevel_folder_id)
  print(surv_dir)
  # test_dir = myCloud.create_dir(myCloud.drive, surv_dir, 'ABC123')
  # myCloud.check_dir(myCloud.drive, myProps.toplevel_folder_id)
  # myCloud.toplevel_dir_exists(myCloud.drive, 'surveillance')
  # print(myCloud.toplevel_dir)       
