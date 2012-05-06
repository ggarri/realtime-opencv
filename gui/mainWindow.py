
__author__="valero"
__date__ ="$17-mar-2011 19:45:57$"

# mainwindow.py

from cvGui import *

try:
   _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
   _fromUtf8 = lambda s: s

from controler import *

class MainWindow(QtGui.QMainWindow):

   """
   Fields
   """
   ui = None
   ctr = None
   mainFilename = None
   backgroundFilename = None
   backgroundColor = None
   brushColor = None
   objectColor = None
   timer = None
   pause = None
   windowCountIndex = None
   windowCountName = None
   

   """
   Methods
   """

   def __init__(self):

      QtGui.QMainWindow.__init__(self)

      self.timer = QtCore.QTimer()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      
      self.__declareConnection()

      
      self.show()
      self.ctr = Controler()

      #Connect the timer with the event
      QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.displayClockUpdate)
      self.timer.start(33)
      self.ctr.display()

      self.pause=0
      self.windowCountIndex = 0
      self.windowCountName = 0
      self.backgroundColor = (0,255,0)
      self.brushColor = (0,255,0)
      self.objectColor = (0,255,0)

      #Add one window to the list
      self.ui.activeWindows_comboBox.addItem("Window0");
      self.ui.activeWindows_comboBox.setCurrentIndex(self.windowCountIndex)

   def __declareConnection(self):

      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap(_fromUtf8("../Resource/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      self.ui.play_pushButton.setIcon(icon)
      
      icon1 = QtGui.QIcon()
      icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../Resource/pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      self.ui.pause_pushButton.setIcon(icon1)

      QtCore.QObject.connect(self.ui.selectPath_toolButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.setMainVideoImage)
      QtCore.QObject.connect(self.ui.selectBackgroundPath_toolButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.setBackgroundVideoImage)
      QtCore.QObject.connect(self.ui.BgTrackselectBackgroundPath_toolButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.setBackgroundVideoImage2)

      QtCore.QObject.connect(self.ui.backgroundColor_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.setBackgroundColor)
      QtCore.QObject.connect(self.ui.trackingBrushColor_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.setBrushColor)
      QtCore.QObject.connect(self.ui.trackingObjectColor_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.setObjectColor)
      QtCore.QObject.connect(self.ui.BgTrackObjectColor_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.setObjectColor)
      QtCore.QObject.connect(self.ui.funObjectColor_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.setObjectColor)
      QtCore.QObject.connect(self.ui.actionNew_Window, QtCore.SIGNAL(_fromUtf8("activated()")),  self.newWindowEvent)
      QtCore.QObject.connect(self.ui.activeWindowsClose_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.closeWindow)
      QtCore.QObject.connect(self.ui.play_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.playEvent)
      QtCore.QObject.connect(self.ui.pause_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.pauseEvent)
      QtCore.QObject.connect(self.ui.vision_tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")),  self.tabSwitch)
      QtCore.QObject.connect(self.ui.clearScreen_pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),  self.clearScreen)
      QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL(_fromUtf8("activated()")),  self.showDialogAbout)
      QtCore.QObject.connect(self.ui.backgroundAlgorithm_comboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.disableColorButton)


   def showDialogAbout(self):
      print "aki"
      self.showDialog("ABOUT","Designed by: \n\nMIGUEL ANGEL VALERO RIVERO and GABRIEL GARRIDO CALVO \n\n\tComputer Vision 2010-11\n\n\t    Hamburg University")

   def showColorDialog(self):

      color = QtGui.QColorDialog.getColor()

      colorRet=None

      if color.isValid():
         colorRet=(color.blue(),color.green(),color.red())

      return colorRet

   def setBrushColor(self):

      bg = self.showColorDialog()

      if bg != None: self.brushColor = bg

      #Put color in correct rgb order
      color = (self.brushColor[2],self.brushColor[1],self.brushColor[0])

      self.ui.trackingBrushColor_pushButton.setStyleSheet("QWidget { background-color: rgb" +  str(color)+"}")


   def setObjectColor(self):

      bg = self.showColorDialog()

      if bg != None: self.objectColor=bg

      #Put color in correct rgb order
      color = (self.objectColor[2],self.objectColor[1],self.objectColor[0])

      self.ui.trackingObjectColor_pushButton.setStyleSheet("QWidget { background-color: rgb" +  str(color)+"}")
      self.ui.BgTrackObjectColor_pushButton.setStyleSheet("QWidget { background-color: rgb" +  str(color)+"}")
      self.ui.funObjectColor_pushButton.setStyleSheet("QWidget { background-color: rgb" +  str(color)+"}")


   def setBackgroundColor(self):

      bg = self.showColorDialog()

      if bg != None: self.backgroundColor = bg
      
      #Put color in correct rgb order
      color = (self.backgroundColor[2],self.backgroundColor[1],self.backgroundColor[0])

      self.ui.backgroundColor_pushButton.setStyleSheet("QWidget { background-color: rgb" +  str(color)+"}")

   def showFileDialog(self):

      filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','../Resource')
      return filename

   def setMainVideoImage(self):

      mainFilename=self.showFileDialog()
      self.ui.videoPath_lineEdit.clear()
      self.ui.videoPath_lineEdit.insert(mainFilename)
      self.ui.selectVideoSource_radioButton.setChecked(True)

   def setBackgroundVideoImage(self):

      backgroundFilename=self.showFileDialog()
      self.ui.selectBackgroundReplacementPath_lineEdit.clear()
      self.ui.selectBackgroundReplacementPath_lineEdit.insert(backgroundFilename)

   def setBackgroundVideoImage2(self):
      backgroundFilename=self.showFileDialog()
      self.ui.BgTrackselectBackgroundPath_lineEdit.clear()
      self.ui.BgTrackselectBackgroundPath_lineEdit.insert(backgroundFilename)

   def disableColorButton(self):
      
      print self.ui.backgroundAlgorithm_comboBox.currentIndex()
      if self.ui.backgroundAlgorithm_comboBox.currentIndex() == 2:
         self.ui.backgroundColor_pushButton.setDisabled(True)
         self.ui.backgroundColor_pushButton.setStyleSheet("QWidget { background-color: transparent }")
      else:
         self.ui.backgroundColor_pushButton.setDisabled(False)
         #Put color in correct rgb order
         color = (self.backgroundColor[2],self.backgroundColor[1],self.backgroundColor[0])
         self.ui.backgroundColor_pushButton.setStyleSheet("QWidget { background-color: rgb" +  str(color)+"}")



   def playEvent(self):

      self.pause=0
      currentWindow = self.ui.activeWindows_comboBox.currentText()
      currentFilter = None
      msg = None
      
      if self.ui.gaussian_radioButton.isChecked():  currentFilter = "GAUSSIAN"
      elif self.ui.median_radioButton.isChecked():    currentFilter = "MEDIAN"
      elif self.ui.canny_radioButton.isChecked():     currentFilter = "CANNY"
      
      """
      bgThresholdSliderValue = self.ui.backgroundThreshold_slider.sliderPosition()
      bgAlgorithm = self.ui.backgroundAlgorithm_comboBox.currentIndex()
      trThresholdValue = self.ui.trackingThreshold_horizontalSlider.sliderPosition()
      trBrushThickValue = self.ui.trackingBrushThick_horizontalSlider.sliderPosition()
      trAlgorithm = self.ui.trackingMethod_comboBox.currentIndex()
      funBrushThickValue = self.ui.funBrushSize_horizontalSlider.sliderPosition()
      funBrushThresholsValue = self.ui.funBrushThreshold_horizontalSlider.sliderPosition()
      """
      if currentWindow == "": msg = "Please select one window in the combo box"

      # WITH CAM
      elif self.ui.selectCamSource_radioButton.isChecked():
         #Background Replace
         if self.ui.vision_tabWidget.currentIndex() == 0:
            backgroundFilename = self.ui.selectBackgroundReplacementPath_lineEdit.text()
            bgThresholdSliderValue = self.ui.backgroundThreshold_slider.sliderPosition()
            bgAlgorithm = self.ui.backgroundAlgorithm_comboBox.currentIndex()
            msg = self.ctr.displayCAM_ReplaceBG(str(currentWindow),str(backgroundFilename),self.backgroundColor,bgThresholdSliderValue,bgAlgorithm,currentFilter)
         #Tracking
         elif self.ui.vision_tabWidget.currentIndex() == 1:
            trThresholdValue = self.ui.trackingThreshold_horizontalSlider.sliderPosition()
            trBrushThickValue = self.ui.trackingBrushThick_horizontalSlider.sliderPosition()
            trAlgorithm = self.ui.trackingMethod_comboBox.currentIndex()

            msg = self.ctr.displayCAMTracking(str(currentWindow), self.objectColor, trThresholdValue, self.brushColor, trBrushThickValue,trAlgorithm, currentFilter)
         #Both
         elif self.ui.vision_tabWidget.currentIndex() == 2:
            backgroundFilename = self.ui.BgTrackselectBackgroundPath_lineEdit.text()
            trThresholdValue = self.ui.BgTrackThreshold_horizontalSlider.sliderPosition()
            trBrushThickValue = self.ui.BgTrackBrushThick_horizontalSlider.sliderPosition()
            trAlgorithm = self.ui.BgTrackMethod_comboBox.currentIndex()
            msg = self.ctr.displayCAM_Tracking_ReplaceBG(str(currentWindow), str(backgroundFilename),self.objectColor,trThresholdValue ,trBrushThickValue,trAlgorithm, currentFilter)
         #Extra
         elif self.ui.vision_tabWidget.currentIndex() == 3:
            #Clearner
            funBrushThresholsValue = self.ui.funBrushThreshold_horizontalSlider.sliderPosition()
            funBrushThickValue = self.ui.funBrushSize_horizontalSlider.sliderPosition()

            if self.ui.clean_radioButton.isChecked():
               msg = self.ctr.displayCAM_Tracking_Clean(str(currentWindow),self.objectColor, funBrushThresholsValue,funBrushThickValue,currentFilter)
            #Lamp
            elif self.ui.lamp_radioButton.isChecked():
               msg = self.ctr.displayCAM_Tracking_Lamp(str(currentWindow),self.objectColor,funBrushThresholsValue,funBrushThickValue,currentFilter)
               
      # WITH SOURCE FILE
      elif self.ui.selectVideoSource_radioButton.isChecked():
         #Background Replace
         mainFilename = self.ui.videoPath_lineEdit.text()
         if self.ui.vision_tabWidget.currentIndex() == 0:
            backgroundFilename = self.ui.selectBackgroundReplacementPath_lineEdit.text()
            bgThresholdSliderValue = self.ui.backgroundThreshold_slider.sliderPosition()
            bgAlgorithm = self.ui.backgroundAlgorithm_comboBox.currentIndex()
            msg = self.ctr.displayVI_ReplaceBG(str(currentWindow),str(mainFilename),str(backgroundFilename),self.backgroundColor,bgThresholdSliderValue,bgAlgorithm,currentFilter)
         #Tracking
         elif self.ui.vision_tabWidget.currentIndex() == 1:
            trThresholdValue = self.ui.trackingThreshold_horizontalSlider.sliderPosition()
            trBrushThickValue = self.ui.trackingBrushThick_horizontalSlider.sliderPosition()
            msg = self.ctr.displayVideoTracking(str(currentWindow), str(mainFilename), self.objectColor, trThresholdValue, self.brushColor, trBrushThickValue,1,currentFilter)

      # IF THERE IS ANY ERROR MESSAGE IS SHOW IN A NEW DIALOG
      if msg != None:
         self.showDialog("WARNING",msg)

   def pauseEvent(self):
      self.pause = 1

   def newWindowEvent(self):
      self.windowCountIndex += 1
      self.windowCountName += 1
      windowName = "Window" + str(self.windowCountName)
      
      self.ui.activeWindows_comboBox.addItem( str(windowName) );
      self.ui.activeWindows_comboBox.setCurrentIndex(self.windowCountIndex)
      
   def closeWindow(self):

      if(self.windowCountIndex > -1):
         currentWinIndex = self.ui.activeWindows_comboBox.currentIndex()
         currenWinName = self.ui.activeWindows_comboBox.currentText()
         self.windowCountIndex -= 1
         self.ui.activeWindows_comboBox.removeItem(currentWinIndex)
         self.ctr.removeWindow(str(currenWinName))
         self.ui.activeWindows_comboBox.setCurrentIndex(self.windowCountIndex)

   def clearScreen(self):
      self.playEvent()

   def displayClockUpdate(self):
      if self.pause==0:
         msg = self.ctr.display()
         if msg != None:
            self.showDialog("WARNING",msg)
      
   def showDialog(self,title,message):
      reply = QtGui.QMessageBox.question(self,title,message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
      return reply

   def tabSwitch(self):

      if self.ui.vision_tabWidget.currentIndex() == 1 or self.ui.vision_tabWidget.currentIndex() == 2 or self.ui.vision_tabWidget.currentIndex() == 3:
         self.ui.clearScreen_pushButton.setDisabled(False)

      else:
         self.ui.clearScreen_pushButton.setDisabled(True)

      if self.ui.vision_tabWidget.currentIndex() == 2 or self.ui.vision_tabWidget.currentIndex() == 3:
         self.ui.selectVideoSource_radioButton.setDisabled(True)
         self.ui.selectCamSource_radioButton.setChecked(True)
         self.ui.selectPath_toolButton.setDisabled(True)
         self.ui.videoPath_lineEdit.setDisabled(True)

      else:
         self.ui.selectVideoSource_radioButton.setDisabled(False)
         self.ui.selectPath_toolButton.setDisabled(False)
         self.ui.videoPath_lineEdit.setDisabled(False)

   def closeEvent(self, event):

      reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
      if reply == QtGui.QMessageBox.Yes:
         event.accept()
         self.ctr.exit();
      else:
         event.ignore()
