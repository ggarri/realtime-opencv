
__author__="Gabriel Garrido Calvo " +"-"+ " Miguel Angel Valero Rivero"
__version__="0.9"
    
from frame import *

"""
@cvar width: Default Value of width (640)
@cvar height: Default Value of width (480)
@cvar fpS: Default Value of Frames Per Second (33)
"""
width = 640
height = 480
fps = 33


class TypeMedia :
   """ Static Class to decribe the source to frames of Media Class
   @cvar CAM: Media Instance with the source of frames from WebCam device.
   @cvar VIDEO: Media Instance with the source of frames from Video file.
   @cvar IMG: Media Instance with the source of frames from Image file.
   """
   CAM = 0
   VIDEO = 1
   IMG = 2

class CAM:
   """ Static Class to get the Port Conection of the WebCam
   @cvar portCAM: Store the reference to WebCam Device
   """
   portCAM = None
   def requestCAM():
      """ Test the conection of the WebCam and if it is not establish yet then 
      it is tried again.
      """
      if CAM.portCAM == None or cv.GetCaptureProperty(CAM.portCAM,cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
         CAM.portCAM = cv.CreateCameraCapture(-1)
      return CAM.portCAM
   requestCAM = staticmethod(requestCAM)
   
class Media:
   """ Manages the frames captured from the source as well as its properties : size,
   number of frames and format.
   @ivar capture: Structure from where the frames are obtained.
   @type capture: cvCapture
   @ivar nFrames: Amount of frames have capture
   @type nFrames: int
   @ivar typeFormat: Type of source where the frames are obtained.
   @type typeFormat: TypeMedia
   """
   __capture = None
   nFrames = 0
   size = None
   typeFormat = None

   
   def __init__(self,path='CAM'):
      """ Initiator of the class Media. It is created a object of this class.
      @keyword path: Indicates which is the source selected. If this field is empty the webcam
      device is chosen.
      """
      if path == 'CAM':
         self.__capture = CAM.requestCAM()
         self.typeFormat = TypeMedia.CAM
         if cv.GetCaptureProperty(self.__capture,cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
            print "ERROR: THE WEBCAM COULD NOT BE INITIALIZED"
      else:
         self.__capture = cv.CreateFileCapture(path)
      
      if self.typeFormat != TypeMedia.CAM:
         # The type of file is determinated like IMAGE or VIDEO
         self.nFrames = cv.GetCaptureProperty(self.__capture,cv.CV_CAP_PROP_FRAME_COUNT)
         if self.nFrames == 1:
            self.typeFormat = TypeMedia.IMG
         else:
            self.typeFormat = TypeMedia.VIDEO
      else:
         self.nFrames = 0

   
   def getFrame (self,n):
      """ The frame located in the chosen position.
         @param n: Number of frame select
         @type n: int
         @return: It is retorned the image which is located in the selected frame
      """
      if n > self.nFrames:
         print "ERROR : Frame Number excess"
         return None
      
      for i in range (n):
         if cv.GrabFrame(self.__capture) == -1:
            print "ERROR : Frame Number excess"
            break;
      
      image = cv.QueryFrame(self.__capture)
      if image != None:
         if self.typeFormat == TypeMedia.CAM:
            cv.Flip(image,image,1)
         # The frame is resized to Standand Value
         thumbnail = cv.CreateMat(height,width , cv.CV_8UC3)
         cv.Resize(image,thumbnail)
         frame = Frame(thumbnail)
         return frame
      
      return None

   def getProperty(self,namePRP):
      """ Gets the select property from the source capture
      @param namePRP: Name of the property
      @type namePRP: cvProperty_id
      @return: Value of the chosen property
      """
      return cv.GetCaptureProperty(self.__capture, namePRP)

   def setProperty(self,namePRP, value):
      """ The provided value is inserted as new value of the property
      @param namePRP: Name of the property
      @type namePRP: cvProperty_id
      @param value: New chosen value
      @type value: Depend on each property
      """
      return cv.SetCaptureProperty(self.__capture, namePRP, value)