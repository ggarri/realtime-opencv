
__author__="Gabriel Garrido Calvo " +"-"+ " Miguel Angel Valero Rivero"
__version__="0.9"


from window import *
from media import *
from frame import *

import types

class Controler:

   __windows = []
   __titles = []
   __frames = []


   def __searchWindow(self,title):
      """ Searches a window already created with the given title if not it is created.
      @param title: Title of window
      @type title: Str
      @return : Index of the window created
      """
      win = None
      for index in range(len(self.__titles) ):
         if self.__titles[index] == title:
            win = self.__windows[index]
            return index
         
      if win == None:
         win = Window(title)
         self.__windows.append(win)
         self.__frames.append([])
         self.__titles.append(title)
         return len(self.__titles)-1
      
      return None

   def __applyFilter(self, frame,filter):
      """ Selects a type of filter and is applied in each frame of this window.
      @param frame: Frame which is applied as filter
      @type frame: Frame
      @param filter: Type of filter to apply
      @type filter: Str[ 'GAUSSIAN', 'MEDIAN', 'CANNY' ].
      """
      if filter == "GAUSSIAN":
         frame.applyFilter(FrameFilter.GAUSSIAN)
      elif filter == "MEDIAN":
         frame.applyFilter(FrameFilter.MEDIAN)
      elif filter == "CANNY":
         frame.applyFilter(FrameFilter.CANNY)

   def display(self):
      """ Shows in each created window the next stored frame
      @note: All created window should have stored frames.
      """
      for index in range(len(self.__windows)):
         if type(self.__frames[index]) == types.FunctionType:
            frame = self.__frames[index]()
            if frame != None:
               self.__windows[index].display(frame,33)
         

   def removeWindow(self,title):
      """ Delete a window with the title as given paramater.
      @param title: Title of the window
      @type title: str
      """
      
      index = self.__searchWindow(title)
      self.__windows[index].close()
      self.__windows.pop(index)
      self.__titles.pop(index)
      self.__frames.pop(index)
      cv.DestroyWindow(title)


   def cloneWindow(self,origWin,dstWin):
      """ Copy from origWin to dstWin all its information except its title.
      @param origWin: Title of original Window
      @type origWin: str
      @param dstWin: Title of destination Window
      @type dstWin: str
      """
      indexWinDst = self.__searchWindow(dstWin)
      indexWinOrg = self.__searchWindow(origWin)
      self.__frames[indexWinDst] = self.__frames[indexWinOrg]


   def displayVideoImage(self, titleWin, path, filter="DISABLE"):
      """ Inserts the frame/s from a file which is selected by the path in the 
      selected windows and it is chosen a type of filter to apply it.
      @param titleWin: Name of window where the frames are strored.
      @type titleWin: str
      @param path: Path of the loaded file.
      @type path: str
      @keyword filter: Type of applied filter.
      @type filter: str
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      vi = Media(path)

      if vi.typeFormat == TypeMedia.VIDEO:
         def displayVideoImage_sub():
            def nextFrame():
               f = vi.getFrame(0)
               if f == None : return None
               self.__applyFilter(f,filter)
               return f
            return nextFrame
         # Store in the vector the executing function to get the frames
         self.__frames[indexWin] = displayVideoImage_sub()
            
      elif vi.typeFormat == TypeMedia.IMG:
         def displayVideoImage_sub(frame):
            def nextFrame():
               self.__applyFilter(frame,filter)
               return frame
            return nextFrame
         # Store in the vector the executing function to get the frames
         self.__frames[indexWin] = displayVideoImage_sub(vi.getFrame(0))


   def displayCAM(self, titleWin, filter="DISABLE"):
      """ Inserts the frame/s from a WebCam devide in the selected windows and 
      it is chosen a type of filter to apply it.
      @param titleWin: Name of window where the frames are strored.
      @type titleWin: str
      @keyword filter: Type of applied filter.
      @type filter: str
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      cam = Media()
      def displayCAM_sub():
         def nextFrame():
            f = cam.getFrame(0)
            self.__applyFilter(f,filter)
            return f
         return nextFrame
      # Store in the vector the executing function to get the frames
      self.__frames[indexWin] = displayCAM_sub()


   def displayVI_ReplaceBG(self,titleWin, pathVI, pathBG, colorDetectBG,threshold, typeDetectBG, filter="DISABLE"):
      """   Inserts the frame/s from a file which is selected by the path in the 
      selected windows. After the background is detected using threshold and colorDetectBG. Can 
      be selected four diferents techniques to detect the Background . The background is 
      replace to the given image or video.Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param pathVI: Path of the loaded file to manipulate.
      @type pathVI: str
      @param pathBG: Path of the loaded file to replace as Background.
      @type pathBG: str
      @param colorDetectBG: Color used to detect the background
      @type colorDetectBG: cvScalar
      @param threshold: Intervale of color to detect the background color
      @type threshold: int [0,255]
      @param typeDetectBG: Technique used to detect background.
      @type typeDetectBG: int [0,4]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      
      """
      indexWin = self.__searchWindow(titleWin)
      vi = Media(pathVI)
      bg = Media(pathBG)
      if vi.nFrames <= 0:
         self.__frames[indexWin] = None
         return "ERROR: THE SOURCE FILE WAS IMPOSSIBLE TO OPEN"
      if bg.nFrames <= 0:
         self.__frames[indexWin] = None
         return "ERROR: THE BACKGROUND FILE WAS IMPOSSIBLE TO OPEN"
      
      print "TYPE" + str(typeDetectBG)
      if vi.typeFormat == TypeMedia.VIDEO:
         lastImage = [vi.getFrame(0).getImage()]
         def displayVI_ReplaceBG_sub():
            if bg.typeFormat == TypeMedia.IMG:
               imgBG = bg.getFrame(0)
               def nextFrame():
                  f = vi.getFrame(0)
                  if f == None : return None
                  if typeDetectBG != 2:    f.replaceBG(colorDetectBG, threshold,imgBG.getImage(), typeDetectBG)
                  else:        f.replaceBG(lastImage, threshold,imgBG.getImage(), typeDetectBG)
                  self.__applyFilter(f,filter)
                  return f
               return nextFrame
            elif bg.typeFormat == TypeMedia.VIDEO:
               def nextFrame():
                  f = vi.getFrame(0)
                  if f == None : return None
                  if bg.getProperty(cv.CV_CAP_PROP_POS_FRAMES)+10 >= bg.nFrames:
                        bg.setProperty(cv.CV_CAP_PROP_POS_FRAMES,0)
                  if typeDetectBG != 2:    f.replaceBG(colorDetectBG, threshold,bg.getFrame(0).getImage(), typeDetectBG)
                  else:        f.replaceBG(lastImage, threshold,bg.getFrame(0).getImage(), typeDetectBG)
                  self.__applyFilter(f,filter)
                  return f
               return nextFrame
         

      elif vi.typeFormat == TypeMedia.IMG:
         f = vi.getFrame(0)
         lastImage = [f.getImage()]
         if f == None : return None
         if bg.typeFormat == TypeMedia.IMG:
            imgBG = bg.getFrame(0)
            def displayVI_ReplaceBG_sub():
               def nextFrame():
                  if typeDetectBG != 2:    f.replaceBG(colorDetectBG, threshold,imgBG.getImage(), typeDetectBG)
                  else:        f.replaceBG(lastImage, threshold,imgBG.getImage(), typeDetectBG)
                  self.__applyFilter(f,filter)
                  return f
               return nextFrame
         if bg.typeFormat == TypeMedia.VIDEO:
            def displayVI_ReplaceBG_sub():
               def nextFrame():
                  f2 = Frame(f.getImage())
                  if bg.getProperty(cv.CV_CAP_PROP_POS_FRAMES)+10 >= bg.nFrames:
                     bg.setProperty(cv.CV_CAP_PROP_POS_FRAMES,0)
                  if typeDetectBG != 2:    f2.replaceBG(colorDetectBG, threshold,bg.getFrame(0).getImage(), typeDetectBG)
                  else:        f2.replaceBG(lastImage, threshold,bg.getFrame(0).getImage(), typeDetectBG)
                  self.__applyFilter(f2,filter)
                  return f2
               return nextFrame

      self.__frames[indexWin] = displayVI_ReplaceBG_sub()





   def displayCAM_ReplaceBG(self,titleWin, pathBG, colorDetectBG,threshold, typeDetectBG, filter="DISABLE"):
      """ Inserts the frame/s from a WebCam device in the selected windows. After the 
      background is detected using threshold and colorDetectBG. Can be selected four 
      diferents techniques to detect the Background . The background is replace to the 
      given image or video.Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param pathBG: Path of the loaded file to replace as Background.
      @type pathBG: str
      @param colorDetectBG: Color used to detect the background
      @type colorDetectBG: cvScalar
      @param threshold: Intervale of color to detect the background color
      @type threshold: int [0,255]
      @param typeDetectBG: Technique used to detect background.
      @type typeDetectBG: int [0,4]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      cam = Media()
      bg = Media(pathBG)
      if cam.getProperty(cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
         self.__frames[indexWin] = None
         return "ERROR: THE CAPTURE DEVICE COULD NOT BE INITIALIZED. \nCheck if you have the webcam connected or it is blocked by another program"
      if bg.nFrames <= 0:
         self.__frames[indexWin] = None
         return "ERROR: THE BACKGROUND FILE WAS IMPOSSIBLE TO OPEN"

      def displayCAM_ReplaceBG_sub():
         #ONLY TO METHOD 2
         lastImage = [cam.getFrame(0).getImage()]
         if bg.typeFormat == TypeMedia.VIDEO:
            def nextFrame():
               f = cam.getFrame(0)
               if bg.getProperty(cv.CV_CAP_PROP_POS_FRAMES)+10 >= bg.nFrames:
                  bg.setProperty(cv.CV_CAP_PROP_POS_FRAMES,0)
               if typeDetectBG != 2:    f.replaceBG(colorDetectBG, threshold,bg.getFrame(0).getImage(), typeDetectBG)
               else:        f.replaceBG(lastImage, threshold,bg.getFrame(0).getImage(), typeDetectBG)
               self.__applyFilter(f,filter)
               return f
            return nextFrame
         elif bg.typeFormat == TypeMedia.IMG:
            imgBG = bg.getFrame(0)
            def nextFrame():
               f = cam.getFrame(0)
               if bg.getProperty(cv.CV_CAP_PROP_POS_FRAMES)+10 >= bg.nFrames:
                  bg.setProperty(cv.CV_CAP_PROP_POS_FRAMES,0)

               if typeDetectBG != 2:    f.replaceBG(colorDetectBG, threshold,imgBG.getImage(), typeDetectBG)
               else:        f.replaceBG(lastImage, threshold,imgBG.getImage(), typeDetectBG)
               
               self.__applyFilter(f,filter)
               return f
            return nextFrame
      self.__frames[indexWin] = displayCAM_ReplaceBG_sub()


   def displayVideoTracking(self,titleWin, pathV, objectColor,threshold, penColor, thickness, typeDetectTrack, filter="DISABLE"):
      """   Inserts the frame/s from a file which is selected by the path in the 
      selected windows. After the tracking realized with a object is detected using 
      threshold and objectColor. Can be selected two diferents techniques to detect the 
      movements of the object . The tracking way is replace to line with selected color 
      and thickness.
      Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param pathV: Path of the loaded file to manipulate.
      @type pathV: str
      @param objectColor: Color used to detect the movements of the object
      @type objectColor: cvScalar
      @param threshold: Intervale of color to detect the object
      @type threshold: int [0,255]
      @param thickness: Thickness to draw the realized movements
      @type thickness: int [0,255]
      @param typeDetectTrack: Technique used to detect the tracking.
      @type typeDetectTrack: int [0,1]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      """

      indexWin = self.__searchWindow(titleWin)
      vi = Media(pathV)
      if vi.nFrames <= 0:
         self.__frames[indexWin] = None
         return "ERROR: THE MAIN FILE WAS IMPOSSIBLE TO OPEN"


      if vi.typeFormat == TypeMedia.VIDEO:
         def displayVideoTracking_sub():
            imgScribble = cv.CreateImage( cv.GetSize(vi.getFrame(0).getImage()), 8, 3)
            point = [None]
            def nextFrame():
               f = vi.getFrame(0)
               if f == None : return None
               f.trackColor(objectColor, threshold, penColor,thickness, point ,imgScribble, typeDetectTrack,0,False)
               self.__applyFilter(f,filter)
               return f
            return nextFrame
      else:
         def displayVideoTracking_sub():
            return None
         
      self.__frames[indexWin] = displayVideoTracking_sub()

      
      
   def displayCAMTracking(self,titleWin, objectColor,threshold, penColor, thickness, typeDetectTrack, filter="DISABLE"):
      """   Inserts the frame/s from a WebCam device in the selected windows. 
      After the tracking realized with a object is detected using 
      threshold and objectColor. Can be selected two diferents techniques to detect the 
      movements of the object . The tracking way is replace to the image background
      and thickness.
      Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param objectColor: Color used to detect the movements of the object
      @type objectColor: cvScalar
      @param threshold: Intervale of color to detect the object
      @type threshold: int [0,255]
      @param thickness: Thickness to draw the realized movements
      @type thickness: int [0,255]
      @param typeDetectTrack: Technique used to detect the tracking.
      @type typeDetectTrack: int [0,1]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      cam = Media()
      if cam.getProperty(cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
         self.__frames[indexWin] = None
         return "ERROR: THE CAPTURE DEVICE COULD NOT BE INITIALIZED. \nCheck if you have the webcam connected or it is blocked by another program"

      def displayCAMTracking_sub():
         imgScribble = cv.CreateImage( cv.GetSize(cam.getFrame(0).getImage()), 8, 3)
         cv.SetZero(imgScribble)
         point = [None]
         def nextFrame():
            f = cam.getFrame(0)
            f.trackColor(objectColor, threshold, penColor,thickness, point ,imgScribble, typeDetectTrack,0,False)
            self.__applyFilter(f,filter)
            return f
         return nextFrame
      
      self.__frames[indexWin] = displayCAMTracking_sub()


   def displayCAM_Tracking_ReplaceBG(self,titleWin,pathBG, objectColor,threshold, thickness, typeDetectTrack, filter="DISABLE"):
      """   Inserts the frame/s from a WebCam device in the selected windows. 
      After the tracking realized with a object is detected using 
      threshold and objectColor. Can be selected two diferents techniques to detect the 
      movements of the object . The background Image is showed by tracking way using the
      thickness.
      Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param pathBG: Path of the background file
      @type pathBG: str
      @param objectColor: Color used to detect the movements of the object
      @type objectColor: cvScalar
      @param threshold: Intervale of color to detect the object
      @type threshold: int [0,255]
      @param thickness: Thickness to draw the realized movements
      @type thickness: int [0,255]
      @param typeDetectTrack: Technique used to detect the tracking.
      @type typeDetectTrack: int [0,1]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      cam = Media()
      bg = Media(pathBG)
      
      if cam.getProperty(cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
         self.__frames[indexWin] = None
         return "ERROR: THE CAPTURE DEVICE COULD NOT BE INITIALIZED. \nCheck if you have the webcam connected or it is blocked by another program"
      if bg.nFrames <= 0:
         self.__frames[indexWin] = None
         return "ERROR: THE BACKGROUND FILE WAS IMPOSSIBLE TO OPEN"

      def displayCAM_Tracking_ReplaceBG_sub():
         if bg.typeFormat == TypeMedia.VIDEO:
            imgScribble = cv.CreateImage( cv.GetSize(cam.getFrame(0).getImage()), 8, 3)
            cv.SetZero(imgScribble)
            point = [None]
            def nextFrame():
               f = cam.getFrame(0)
               f.trackColor(objectColor, threshold, objectColor,thickness, point ,imgScribble, typeDetectTrack,1,False)
               if bg.getProperty(cv.CV_CAP_PROP_POS_FRAMES)+10 >= bg.nFrames:
                  bg.setProperty(cv.CV_CAP_PROP_POS_FRAMES,0)
               f.replaceBG(objectColor, 10,bg.getFrame(0).getImage(), 0)
               self.__applyFilter(f,filter)
               return f
            return nextFrame
         if bg.typeFormat == TypeMedia.IMG:
            imgScribble = cv.CreateImage( cv.GetSize(cam.getFrame(0).getImage()), 8, 3)
            cv.SetZero(imgScribble)
            point = [None]
            imgBG = bg.getFrame(0)
            def nextFrame():
               f = cam.getFrame(0)
               f.trackColor(objectColor, threshold, objectColor,thickness, point ,imgScribble, typeDetectTrack,1,False)
               f.replaceBG(objectColor, 10,imgBG.getImage(), 0)
               self.__applyFilter(f,filter)
               return f
            return nextFrame

      self.__frames[indexWin] = displayCAM_Tracking_ReplaceBG_sub()



   def displayCAM_Tracking_Clean(self,titleWin, objectColor,threshold, thickness, filter="DISABLE"):
      """ Inserts the frame/s from a WebCam device in the selected windows. 
      After the tracking realized with a object is detected using 
      threshold and objectColor. The WebCam Image is showed in the zones where the object
      have been detected.
      Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param objectColor: Color used to detect the movements of the object
      @type objectColor: cvScalar
      @param threshold: Intervale of color to detect the object
      @type threshold: int [0,255]
      @param thickness: Thickness to draw the realized movements
      @type thickness: int [0,255]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      cam = Media()
      if cam.getProperty(cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
         self.__frames[indexWin] = None
         return "ERROR: THE CAPTURE DEVICE COULD NOT BE INITIALIZED. \nCheck if you have the webcam connected or it is blocked by another program"

      def displayCAM_Tracking_Clean_sub():
         point = [None]
         imgScribble = cv.CreateImage( cv.GetSize(cam.getFrame(0).getImage()), 8, 3)
         cv.SetZero(imgScribble)
         def nextFrame():
            f = cam.getFrame(0)
            f.trackClean(objectColor, threshold, thickness, point,imgScribble)
            self.__applyFilter(f,filter)
            return f
         return nextFrame
      self.__frames[indexWin] = displayCAM_Tracking_Clean_sub()

      

   def displayCAM_Tracking_Lamp(self,titleWin, objectColor,threshold, thickness, filter="DISABLE"):
      """ Inserts the frame/s from a WebCam device in the selected windows. 
      After the tracking realized with a object is detected using 
      threshold and objectColor. The WebCam Image is showed in the zone where the object
      is detected and the thickness is used to chosse the size of the zone.
      Also it is chosen a type of filter to apply it.
      @param titleWin: Title of the window where to show
      @type titleWin: str
      @param objectColor: Color used to detect the movements of the object
      @type objectColor: cvScalar
      @param threshold: Intervale of color to detect the object
      @type threshold: int [0,255]
      @param thickness: Thickness to draw the realized movements
      @type thickness: int [0,255]
      @keyword filter: Type of applied filter
      @type filter: str ['GAUSSIAN','MEDIAN','CANNY']
      @note: If the select window dont exist, it is created
      """
      indexWin = self.__searchWindow(titleWin)
      cam = Media()
      if cam.getProperty(cv.CV_CAP_PROP_FRAME_WIDTH) == 0.0:
         self.__frames[indexWin] = None
         return "ERROR: THE CAPTURE DEVICE COULD NOT BE INITIALIZED. \nCheck if you have the webcam connected or it is blocked by another program"

      point = [None]
      def displayCAM_Tracking_Lamp_sub():
         def nextFrame():
            f = cam.getFrame(0)
            if f == None : return None
            f.trackLamp(objectColor, threshold, thickness, point)
            self.__applyFilter(f,filter)
            return f
         return nextFrame
      self.__frames[indexWin] = displayCAM_Tracking_Lamp_sub()


   def exit(self):
      cv.DestroyAllWindows()