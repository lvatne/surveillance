import survprop
import cloud
import datehelper
import localstorage
import os
import datetime as dt
from googleapiclient.http import MediaFileUpload

class ImageUploader:

  # def __init__(self):      

  def establish_dir(self):
      myProps = survprop.SurvProp()
      self.props = myProps
      myCloud = cloud.Cloud(myProps)
      self.cloud = myCloud
      surv_dir = myCloud.dir_exists(myCloud.drive, myProps.toplevel_folder_id, myProps.surveillance_folder_name)
      dh = datehelper.DateHelper()
      surv_dir = myCloud.check_dir(myCloud.drive, myProps.toplevel_folder_id)
      day_dir = None
      if (surv_dir):
          year_dir = myCloud.dir_exists(myCloud.drive, surv_dir, dh.year())
          if not year_dir:
              year_dir = myCloud.create_dir(myCloud.drive, surv_dir, dh.year())
          month_dir = myCloud.dir_exists(myCloud.drive, year_dir, dh.month())
          if not month_dir:
              month_dir = myCloud.create_dir(myCloud.drive, year_dir, dh.month())
          day_dir = myCloud.dir_exists(myCloud.drive, month_dir, dh.day())
          if not day_dir:
              day_dir = myCloud.create_dir(myCloud.drive, month_dir, dh.day())
      return day_dir
    

  def find_localdir(self):
    LS = localstorage.LocalStorage()
    return LS.current_dir()


  def upload_jpeg(self, filename, file, parent_id) :        
        file_metadata = {'name': filename,
                         'parents':[parent_id]
                         }
        media = MediaFileUpload(file, mimetype='image/jpeg')
        # pylint: disable=maybe-no-member
        file = self.cloud.drive.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        file_id = file['id']
        self.cloud.share_file(file_id)
        print(file)
        return file

    
  def upload_mpeg(self, filename, file, parent_id) :        
        file_metadata = {'name': filename,
                         'parents':[parent_id]
                         }
        media = MediaFileUpload(file, mimetype='video/mp4')
        # pylint: disable=maybe-no-member
        file = self.cloud.drive.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        file_id = file['id']
        self.cloud.share_file(file_id)
        print(file)
        return file


  
    
if __name__ == '__main__':
  uploader = ImageUploader()
  day_dir = uploader.establish_dir()
  local_dir = uploader.find_localdir()
  now = dt.datetime.now()
  ago = now-dt.timedelta(minutes=uploader.props.interval)

  for root, dirs,files in os.walk(local_dir):  
    for fname in files:
        path = os.path.join(root, fname)
        st = os.stat(path)    
        mtime = dt.datetime.fromtimestamp(st.st_mtime)
        if mtime > ago:
          print('%s modified %s'%(path, mtime))
          if fname.endswith('mp4'):
            uploader.upload_mpeg(fname, path, day_dir)
          else:
            uploader.upload_jpeg(fname, path, day_dir)
  
  
