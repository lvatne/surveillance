import numpy
import os
import time
import localstorage
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize, imshow

class VideoMaker:
    def __init__(self, imgDirName):
        # Check if the image directory actually exists
        if os.path.isdir(imgDirName):
            fName = os.path.basename(os.path.dirname(imgDirName)) + '.mp4'
            outFileName = os.path.join(imgDirName, fName)
            if os.path.isfile(outFileName):
                print('File already exists: ', outFileName)
            else:
                size = (480, 270)
                # print('Basename: ', os.path.basename(imgDirName))
                fourcc = VideoWriter_fourcc('H','2','6','4')
                # print(fourcc)
                self.VidWriter = VideoWriter(outFileName, fourcc, 4.0, size)
                for filename in sorted(os.listdir(imgDirName)):
                    absname = os.path.join(imgDirName, filename)
                    if absname != outFileName:
                        cap = imread(absname)
                        cap2 = resize(cap, size)
                        self.VidWriter.write(cap2)
                self.VidWriter.release()
        
        

if __name__ == "__main__":
    # homePath = os.environ['HOMEPATH']
    # pictPath = os.path.join(homePath, 'Pictures')
    ls = localstorage.LocalStorage()
    imgPath = ls.current_dir()
    vMaker = VideoMaker(imgPath)
