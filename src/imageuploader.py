import survprop
import cloud
import datehelper

class ImageUploader:

  # def __init__(self):      

  def establish_dir(self):
      myProps = survprop.SurvProp()
      myCloud = cloud.Cloud(myProps)
      surv_dir = myCloud.dir_exists(myCloud.drive, myProps.toplevel_folder_id, myProps.surveillance_folder_name)
      dh = datehelper.DateHelper()
      surv_dir = myCloud.dir_exists(myCloud.drive, myProps.toplevel_folder_id, myProps.surveillance_folder_name)
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
    
    
if __name__ == '__main__':
  uploader = ImageUploader()
  day_dir = uploader.establish_dir()
  
