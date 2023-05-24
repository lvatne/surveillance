import json

class SurvProp:
    properties_file = '/opt/surveillance/surveillance/conf/survprops.json'
    credentials_file = None
    client_secret_file = None

    def __init__(self):
        with open(self.properties_file) as json_file:
            self.data = json.load(json_file)
            self.credentials_file = self.data['credentials_file']
            self.client_secret_file = self.data['client_secret_file']

    def __str__(self):
            return str(self.data)
        


if __name__ == '__main__':
  myProps = SurvProp()
  print(myProps)