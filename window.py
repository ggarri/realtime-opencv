
__author__="Gabriel Garrido Calvo " +"-"+ " Miguel Angel Valero Rivero"
__version__="0.9"


from frame import *


class Window:
   """Models the using of screen"""

   title = None
   size = None 


   def __init__(self, title, sizeX = 640, sizeY = 480):
      """ Initiator of the class Window. It is created a new window using OpenCv with title and
      values selected.
      @param title:	Window title assigned
      @type title: str
      @keyword sizeX:	Size of the x component of the window. Default value 640
      @type sizeX:   int
      @keyword sizeY:	Size of the y component ot the window. Default value 480
      @type sizeY:   int
      """

      self.title = title
      self.size = (sizeX, sizeY)
      cv.NamedWindow(self.title, cv.CV_WINDOW_AUTOSIZE)
      cv.ResizeWindow(self.title, sizeX, sizeY)


   def display(self, frame, wait=0):
      """ Module to display the frame in a Window created previusly.
      @param frame:	The image that will be shown in the window
      @type frame:   Frame
      @keyword wait:   Wait time between images
      @type wait: int
      @return:		Pressed key during wait
      """
      if frame != None:
         cv.ShowImage(self.title, frame.getImage())
      char = cv.WaitKey(wait)
      return char

   def createTrackBar(self,barId, length, refProc):
      """ Creates a trackbar in the bottom of the window, controlling the procedure 
      referenced by refProc
      @param barId:	Identificator of the trackbar
      @type barId : str
      @param length:	Trackbar intervale [0,lenght]
      @type length: int
      @param refProc:	Name of the procedure executed when a event is appeared
      @type refProc: function
      """

      cv.CreateTrackbar(barId,self.title,0,length,refProc)

   def getTrackBarValue(self, barId):
      """Gets the current trackbar value
      @param barId:	Identificator of the trackbar
      @type barId:   str
      @return: Current value of the TrackBar
      """
      cv.GetTrackbarPos(barId,self.title)

   def setTrackBarValue(self, barId, value):
      """Sets the current trackbar value
      @param barId:	Identificator of the trackbar
      @type barId:   str
      @param value:	New value to assign to TrackBar
      @type value: int
      """

      cv.SetTrackbarPos(barId, self.title, value)

   def close(self):
      """Closes and destroys the window"""
      cv.DestroyWindow(self.title)
