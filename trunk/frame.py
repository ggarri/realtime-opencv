
__author__="Gabriel Garrido Calvo " +"-"+ " Miguel Angel Valero Rivero"
__version__="0.9"

import os
import platform


try:
   arquitecture = platform.architecture()[0]
   OS = os.uname()[0]
   if OS == 'Linux':
      if arquitecture == '32bit':
         import libLINUX.cv as cv
      else:
         import libLINUX.x64.cv as cv
   elif OS == 'Darwin':
      if arquitecture == '32bit':
         import libMac.cv as cv
      else:
         import libMac.x64.cv as cv
   else:
      import cv
except:
   try:
      import cv
   except:
      print "ERROR: This program works only on LINUX or MAC. Version 2.6.0 OPENCV"

import math


# Types of filters
class FrameFilter:
   """ Static class where is selected the type of filter to apply
   @cvar DISABLE: None filter to apply
   @cvar GAUSSIAN: Gaussian filter to apply- Linear convolution with a 9x9 Gaussian kernel
   @cvar MEDIAN: Median filter with a 9x9 Square aperture
   @cvar CANNY: Algorithm for edge detection.
   """
   DISABLE = 0
   GAUSSIAN = 1
   MEDIAN = 2
   CANNY = 3

class Frame:
   """ Keeps the information about each frame before to display. This class applys the
   different filters and techniques of detection of background and tracking on the image
   @ivar image: Stores the frame information.
   """
   __image = None


   def __init__(self,iplI):
      """ Initiator of the class Frame. It is stored the information about a IplImage
      @param iplI: Information of the image to store
      @type iplI: IpLImage or cvMat
      """
      self.__image = cv.CloneMat(iplI)

   def getImage(self):
      """ Gets the stored image
      @return: IpLImage or cvMat
      """
      return self.__image


   def applyFilter(self,typeF):
      """ Applies filter to the stored image
      @param typeF: The type the filter to apply
      @type typeF: FrameFilter {GAUSSIAN,MEDIAN,CANNY}
      """
      if typeF == FrameFilter.GAUSSIAN:
         cv.Smooth(self.__image,self.__image,cv.CV_GAUSSIAN,9,9)
      elif typeF == FrameFilter.MEDIAN:
         cv.Smooth(self.__image,self.__image,cv.CV_MEDIAN,9)
      elif typeF == FrameFilter.CANNY:
         frame2 = cv.CreateImage(cv.GetSize(self.__image),8,1)
         cv.CvtColor(self.__image,frame2,cv.CV_BGR2GRAY)
         cv.Canny(frame2,frame2,70.0,140.0,3)
         cv.CvtColor(frame2,self.__image,cv.CV_GRAY2BGR)

   def replaceBG(self,colorToReplace, threshold,imageBG, typeBG):
      """ Replaces the background color with the specified image. So that it is 
      used a amount of threshold to detected the background color and different method 
      to detect it. 
      @param colorToReplace: Color used to detect the Background
      @type colorToReplace: cvScalar
      @param threshold: Threshould used as the edge to detect Background.
      @type threshold: int or IplImage
      @param imageBG: The image used as new Background
      @type imageBG: IplImage
      @param typeBG: Select type of technique to detect the Background   
      @param typeBG: int{0,1,2 or 3}
      @note: If the used technique is 2, the colorToReplace must be a another IpLImage

      """
      BG = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      if typeBG == 0:
         BG,grayI = self.__getBackGround(threshold,colorToReplace)
      elif typeBG == 1:
         BG,grayI = self.__getBackGround1(threshold,colorToReplace)
      elif typeBG == 2:
         BG,grayI = self.__getBackGround2(threshold,colorToReplace[0])
         colorToReplace[0] = cv.CloneMat(cv.GetMat(self.__image))
      elif typeBG == 3:
         BG,grayI = self.__getBackGround3(threshold,colorToReplace)

      cv.Not(grayI,grayI)
      cv.Add(BG,imageBG,self.__image,grayI)

      #----- GRAY SCALE DISPLAY (pixel white to replace)
      #cv.CvtColor(grayI,self.__image,cv.CV_GRAY2BGR)
      #----- REPLACE BG DISPLAY (pixel black to replace)
      #self.__image = cv.CloneMat(cv.GetMat(BG))

   def __getBackGround(self,threshold,color):
      """ Method number 1 to detect the background pixels. The background is detected of 
      the local Image using given color. For this it is calculed
      the difference between local Image and another image set up the given color only.
      @param threshold: Edge to detect the color background
      @type threshold: int
      @param color: Color used to detect background
      @type color: cvScalar
      @return: As first parameter the original image changing the different pixel to black pixel.
      As Second parameter a IplImage in Gray Scale where the differences are white pixels. After 
      this can be used as mask.
      
      """
      differenceI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      grayI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 1)
      backgroundI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      cv.Set(backgroundI,color)

      cv.AbsDiff(self.__image,backgroundI,differenceI)
      cv.CvtColor(differenceI,grayI,cv.CV_BGR2GRAY)
      cv.Smooth(grayI,grayI,cv.CV_BLUR,5)
      cv.Smooth(grayI,grayI,cv.CV_MEDIAN,5)

      cv.Threshold(grayI,grayI,threshold, 255, cv.CV_THRESH_BINARY )
      cv.SetZero(differenceI)
      cv.And(self.__image,self.__image,differenceI,grayI)
      return differenceI,grayI
      #return grayI

   def __getBackGround1(self,threshold,color):
      """ Method number 2 to detect the background pixels. The background is detected of 
      the local Image using given color. For this it is calculed
      the difference between local Image and another image set up the given color only in 
      each one channel of color.
      @param threshold: Edge to detect the color background
      @type threshold: int
      @param color: Color used to detect background
      @type color: cvScalar
      @return: As first parameter the original image changing the different pixel to black pixel.
      As Second parameter a IplImage in Gray Scale where the differences are white pixels. After 
      this can be used as mask.
      """

      backgroundI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      cv.Set(backgroundI,color)

      i0,i1,i2,i3,b0,b1,b2,b3,d0,d1,d2,d3 = tuple([cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 1) for i in range(12)])

      differenceI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      grayI = cv.CreateImage(cv.GetSize(differenceI), cv.IPL_DEPTH_8U, 1)

      cv.Split(self.__image,i0,i1,i2,None)
      cv.Split(backgroundI,b0,b1,b2,None)

      cv.AbsDiff(i0,b0,d0)
      cv.AbsDiff(i1,b1,d1)
      cv.AbsDiff(i2,b2,d2)

      cv.Threshold(d0,d0,threshold, 255, cv.CV_THRESH_BINARY )
      cv.Threshold(d1,d1,threshold, 255, cv.CV_THRESH_BINARY )
      cv.Threshold(d2,d2,threshold, 255, cv.CV_THRESH_BINARY )

      cv.Merge(d0,d1,d2,None,differenceI)
      cv.CvtColor(differenceI,grayI,cv.CV_BGR2GRAY)

      cv.Smooth(grayI,grayI,cv.CV_BLUR,5)
      cv.Smooth(grayI,grayI,cv.CV_MEDIAN,5)
      cv.Threshold(grayI,grayI,threshold, 255, cv.CV_THRESH_BINARY)

      cv.SetZero(differenceI)
      
      cv.Add(self.__image,differenceI,differenceI,grayI)
      
      return differenceI,grayI
      


   def __getBackGround2(self,threshold,preImage):
      """ Method number 3 to detect the background pixels. The background is detected of 
      the local Image using the given preImage. For this it is calculed the difference 
      between them.
      @type threshold: int
      @param preImage: Image used to compare the differences
      @type preImage: IplImage
      @return: As first parameter the original image changing the different pixel to black pixel.
      As Second parameter a IplImage in Gray Scale where the differences are white pixels. After 
      this can be used as mask.
      """

      
      differenceI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      grayI = cv.CreateImage(cv.GetSize(differenceI), cv.IPL_DEPTH_8U, 1)

      cv.AbsDiff(self.__image,preImage,differenceI)
      cv.CvtColor(differenceI,grayI,cv.CV_BGR2GRAY)

      cv.Threshold(grayI,grayI,threshold, 255, cv.CV_THRESH_BINARY  )
      cv.Smooth(grayI,grayI,cv.CV_MEDIAN,5)
      cv.Smooth(grayI,grayI,cv.CV_GAUSSIAN,5)

      cv.SetZero(differenceI)
      cv.Add(self.__image,differenceI,differenceI,grayI)
      return differenceI,grayI

   def __getBackGround3(self,threshold,color):
      """ Method number 4 to detect the background pixels. Detect the background 
      comparing each pixel of local image with the given color using the threshold. 
      (TOO SLOW)
      @param threshold: Edge to detect the color background
      @type threshold: int
      @param color: Color used to detect background
      @type color: cvScalar
      @return: As first parameter the original image changing the different pixel to black pixel.
      As Second parameter a IplImage in Gray Scale where the differences are white pixels. After 
      this can be used as mask.
      """
      def intervale(id1,id2):
         if math.fabs(id1-id2) < threshold:
            return True
         return False

      differenceI = cv.CloneMat(self.__image)
      size = cv.GetSize(self.__image)
      grayI = cv.CreateImage(cv.GetSize(differenceI), cv.IPL_DEPTH_8U, 1)
      cv.SetZero(grayI)
      for i in range(0, size[0]):
         for j in range(0, size[1]):
            pixel = cv.Get2D(self.__image,j,i)
            if intervale(color[0],pixel[0]) and intervale(color[1],pixel[1]) and intervale(color[2],pixel[2]):
               cv.Set2D(differenceI,j,i,cv.Scalar(0,0,0))
               cv.Set2D(grayI,j,i,cv.Scalar(255,255,255))

      cv.Not(grayI,grayI)
      return differenceI,grayI


   def trackColor(self, objectColor, threshold, penColor, thickness, lastPoint2,imgScribble,typeS,typeDraw,disable):
      """ Applies the technique of tracking to local image. For this it is used the color
      of the followed object to draw the track in the image. It is possible apply two differents
      techniques to follow the object and also thickness is chosen. (ONLY WEBCAM)
      @param objectColor: Color of the used object to detect.
      @type objectColor: cvScalar
      @param threshold: Threshould detected color of the object.
      @type threshold: int [0,255]
      @param penColor: Drawing used color
      @type penColor: cvScalar
      @param thickness: Thickness used to draw.
      @type thickness: int [0,255]
      @param lastPoint2: Auxiliar Object
      @param imgScribble: Image where is stored the tracking way.
      @type imgScribble: IplImage
      @param typeS: Type of method used to detect the object
      @type typeS: int[0,1]
      @param typeDraw: If 1 the transparence is disabled.
      @param disable: Parameter of pause option
      """
      lastPoint = lastPoint2[0]
      #penColor = objectColor
      imgThresh = None
      if typeS == 1:
         lowerColor = cv.Scalar(objectColor[0]-threshold,objectColor[1]-threshold,objectColor[2]-threshold)
         upperColor = cv.Scalar(objectColor[0]+threshold,objectColor[1]+threshold,objectColor[2]+threshold)
         imgThresh = self.__getThresholdImage(lowerColor,upperColor)
      elif typeS == 0:
         imgThresh = self.__getThresholdImage1(threshold,objectColor)

      moments = cv.Moments(imgThresh,1)
      moment10 = cv.GetSpatialMoment(moments, 1, 0)
      moment01 = cv.GetSpatialMoment(moments, 0, 1);
      area = cv.GetCentralMoment(moments, 0, 0);
      #print area

      if area == 0 or disable == True:
         currentPoint = None
      else:
         currentPoint = [moment10/area,moment01/area]
         
      if lastPoint != None and currentPoint != None:
         cv.Line(imgScribble, (int(currentPoint[0]), int(currentPoint[1])), (int(lastPoint[0]), int(lastPoint[1])), penColor, thickness,cv.CV_AA)


      mask = cv.CreateImage(cv.GetSize(self.__image), 8, 1)
      cv.CvtColor(imgScribble, mask, cv.CV_BGR2GRAY)
      cv.Threshold(mask,mask,20, 255, cv.CV_THRESH_BINARY  )
      cv.Not(mask,mask)
      blackI = cv.CreateImage(cv.GetSize(self.__image), 8, 3)
      cv.SetZero(blackI)
      cv.And(self.__image,self.__image,blackI,mask)
      
      if typeDraw == 0:# Totally Transparent
         cv.Add(self.__image, imgScribble, self.__image)
      else: # Totally Opaque
         cv.Add(blackI, imgScribble, self.__image)
      #self.__image = blackI
      
      lastPoint2[0] = currentPoint


   ## LIMPIAR
   def trackClean(self, objectColor, threshold, thickness, lastPoint2,imgScribble):
      """ Applies the technique of tracking to local image with the method of to clear. 
      For this it is used the color of the followed object to show the lowed image.(ONLY WEBCAM)
      @param objectColor: Color of the used object to detect.
      @type objectColor: cvScalar
      @param threshold: Threshould detected color of the object.
      @type threshold: int [0,255]
      @param thickness: Thickness used to draw.
      @type thickness: int [0,255]
      @param lastPoint2: Auxiliar Object
      @param imgScribble: Image where is stored the tracking way.
      @type imgScribble: IplImage
      """

      lastPoint = lastPoint2[0]
      imgThresh = self.__getThresholdImage1(threshold,objectColor)
      moments = cv.Moments(imgThresh,1)
      moment10 = cv.GetSpatialMoment(moments, 1, 0)
      moment01 = cv.GetSpatialMoment(moments, 0, 1)
      area = cv.GetCentralMoment(moments, 0, 0)
      #print area

      if area == 0:
         currentPoint = None
      else:
         currentPoint = [moment10/area,moment01/area]

      if lastPoint != None and currentPoint != None:
         cv.Line(imgScribble, (int(currentPoint[0]), int(currentPoint[1])), (int(lastPoint[0]), int(lastPoint[1])), cv.Scalar(250,250,250), thickness,cv.CV_AA)

      mask = cv.CreateImage(cv.GetSize(self.__image), 8, 1)
      cv.SetZero(mask)
      cv.CvtColor(imgScribble, mask, cv.CV_BGR2GRAY)
      blackI = cv.CreateImage(cv.GetSize(self.__image), 8, 3)
      cv.SetZero(blackI)
      cv.And(self.__image,self.__image,blackI,mask)
      self.__image = blackI
      lastPoint2[0] = currentPoint


   # MODO LINTERNA
   def trackLamp(self, objectColor, threshold, thickness, lastPoint2):
      """ Applies the technique of tracking to local image with the method of to clear. 
      For this it is used the color of the followed object to show the lowed image only
      in the current position. (ONLY WEBCAM)
      @param objectColor: Color of the used object to detect.
      @type objectColor: cvScalar
      @param threshold: Threshould detected color of the object.
      @type threshold: int [0,255]
      @param thickness: Thickness used to draw.
      @type thickness: int [0,255]
      @param lastPoint2: Auxiliar Object
      """

      lastPoint = lastPoint2[0]
      imgThresh = self.__getThresholdImage1(threshold,objectColor)
      moments = cv.Moments(imgThresh,1)
      moment10 = cv.GetSpatialMoment(moments, 1, 0)
      moment01 = cv.GetSpatialMoment(moments, 0, 1);
      area = cv.GetCentralMoment(moments, 0, 0);

      if area == 0:
         currentPoint = None
      else:
         currentPoint = [moment10/area,moment01/area]

      mask = cv.CreateImage(cv.GetSize(self.__image), 8, 1)
      cv.SetZero(mask)
      if lastPoint != None and currentPoint != None:
         cv.Line(mask, (int(currentPoint[0]), int(currentPoint[1])), (int(lastPoint[0]), int(lastPoint[1])), cv.Scalar(250,250,250), thickness,cv.CV_AA)

      #cv.CvtColor(imgScribble, mask, cv.CV_BGR2GRAY)
      blackI = cv.CreateImage(cv.GetSize(self.__image), 8, 3)
      cv.SetZero(blackI)
      cv.And(self.__image,self.__image,blackI,mask)
      self.__image = blackI
      lastPoint2[0] = currentPoint
      

   def __getThresholdImage(self,colorLower,colorUpper):
      """ Tecnique number 1 to detect the current possition of a specific color
      in the local image.
         @param colorLower: This is Low value of the intervale of colour to search.
         @param colorUpper: This is Hight value of the intervale of colour to search.
         @return The mask where is found the intervale of chosen colours.
      """
      imgHSV = cv.CreateImage(cv.GetSize(self.__image), 8, 3)
      cv.CvtColor(self.__image, imgHSV, cv.CV_BGR2HSV)
      imgResult = cv.CreateImage(cv.GetSize(self.__image), 8, 1)
      cv.InRangeS(self.__image, colorLower, colorUpper, imgResult)
      return imgResult

   def __getThresholdImage1(self,threshold, color):
      """ Tecnique number 2 to detect the current possition of a specific color
      in the local image.
         @param threshold: Allowed threshold to search.
         @param color: Value of the color to search.
         @return The mask where is found the intervale of chosen colours.
      """
      differenceI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      grayI = cv.CreateImage(cv.GetSize(differenceI), cv.IPL_DEPTH_8U, 1)
      backgroundI = cv.CreateImage(cv.GetSize(self.__image), cv.IPL_DEPTH_8U, 3)
      cv.Set(backgroundI,color)
      cv.AbsDiff(self.__image,backgroundI,differenceI)
      cv.CvtColor(differenceI,grayI,cv.CV_BGR2GRAY)
      cv.Smooth(grayI,grayI,cv.CV_BLUR,5)
      cv.Smooth(grayI,grayI,cv.CV_MEDIAN,5)
      cv.Threshold(grayI,grayI,threshold, 255, cv.CV_THRESH_BINARY )
      cv.Not(grayI,grayI)
      
      return grayI
