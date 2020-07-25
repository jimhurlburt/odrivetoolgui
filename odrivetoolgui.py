import sys, time

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from ui_odrive import Ui_Odrive

import odrive
import odrive.enums

#***************************************************************************

class OdriveToolGui:

   def __init__(self):
      app = QApplication(sys.argv)
      self.window = QMainWindow()
      self.ui = Ui_Odrive()
      self.ui.setupUi(self.window)

      self.drive = ""
      self.axis = ""

      (self.dEnums, self.dAxisError, self.dMotorError,
       self.dEncoderError, self.dControllerError) = getenums()

      self.ui.actionFind_any.triggered.connect(self.findanyodrive)
      self.ui.actionFind_on_port.triggered.connect(self.findonport)
   
      self.ui.actionAxis0.triggered.connect(self.calibrateAxis0)
      self.ui.actionAxis1.triggered.connect(self.calibrateAxis1)

      self.ui.Save_button.clicked.connect(self.axisSave)
      self.ui.Calibrate_button.clicked.connect(self.runAxisCalibrate)
      self.ui.axis_conf_Close_button.clicked.connect(self.close_cal_frame)
   
      self.ui.actionexit.triggered.connect(app.exit)
   
      self.ui.Basic_calibration.hide()

      self.window.show()
      sys.exit(app.exec_())


   #*** OdriveToolGui.__init__******************************

   def findanyodrive(self):
      print("Find an odrive")

      self.port = False
      self.drive = odrive.find_any()

      self.ui.drive_label.setText("Odrive {} found".format(self.drive.serial_number))
      print(self.drive.serial_number)
      #print(self.drive.axis0.motor)
      #print(dir(self.drive.axis0.motor))

   #*** OdriveToolGui.findanyodrive ************************

   def calibrateAxis0(self):

      self.ui.configframelabel.setText("Axis 0")
      self.axis = self.drive.axis0
      self.calibrateAxis()

   #*** OdriveToolGui.calibrateAxis0 ***********************

   def calibrateAxis1(self):

      self.ui.configframelabel.setText("Axis 1")
      self.axis = self.drive.axis1
      self.calibrateAxis()

   #*** OdriveToolGui.calibrateAxis1 ***********************

   def calibrateAxis(self):
   
      self.ui.Basic_calibration.show()
   
      self.ui.Current_Lim.setText(str(self.axis.motor.config.current_lim))
      self.ui.Calibrate_current.setText(
         str(self.axis.motor.config.calibration_current))
      
      self.ui.Vel_limit.setText(str(self.axis.controller.config.vel_limit))
      self.ui.Brake_resistance.setText(
         "{0:5.3f}".format(self.drive.config.brake_resistance))
      
      self.ui.Pole_pairs.setText(str(self.axis.motor.config.pole_pairs))
      self.ui.Encoder_cnt_rev.setText(str(self.axis.encoder.config.cpr))

      self.ui.Motor_type.setCurrentIndex(self.axis.motor.config.motor_type)

   #*** OdriveToolGui.calibrateAxis ************************

   def findonport(self, event):
      
      print("Find an odrive on /dev/ttyS0")
      self.port = "serial:/dev/ttyS0"
      drive0 = odrive.find_any(self.port)
      print(self.drive.serial_number)

   #*** OdriveToolGui.findonport ****************************
   
   def close_cal_frame(self):
      self.ui.Basic_calibration.hide()

   #*** OdriveToolGui.close_cal_frame **********************

   def runAxisCalibrate(self):
      self.axis.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE

      dErrors = self.checkerrors()

      if dErrors:
         print(dErrors)

   #*** OdriveToolGui.runAxisCalibrate *********************

   def axisSave(self):
      print("save button")
      self.ui.drive_label.setText("Save & reboot odrive")
      self.ui.drive_label.repaint()

         
      print(float(self.ui.Current_Lim.text()),
            float(self.ui.Calibrate_current.text()),
            float(self.ui.Vel_limit.text()),
            float(self.ui.Brake_resistance.text()),
            int(self.ui.Pole_pairs.text()),
            int(self.ui.Encoder_cnt_rev.text()),
            self.ui.Motor_type.currentIndex())

      self.axis.motor.config.current_lim = float(self.ui.Current_Lim.text())
      self.axis.motor.config.calibration_current = \
                   float(self.ui.Calibrate_current.text())
      
      self.axis.controller.config.vel_limit = float(self.ui.Vel_limit.text())
      self.drive.config.brake_resistance = \
                   float(self.ui.Brake_resistance.text())
      
      self.axis.motor.config.pole_pairs = int(self.ui.Pole_pairs.text())
      self.axis.encoder.config.cpr = int(self.ui.Encoder_cnt_rev.text())
      self.axis.motor.config.motor_type = self.ui.Motor_type.currentIndex()

      self.drive.save_configuration()
      
      try:
         self.drive.reboot()

      except:
         pass
      
      if self.port:
         self.drive = odrive.find_any(self.port)

      else:
         self.drive = odrive.find_any()

      self.ui.drive_label.setText("Odrive {} found".format(self.drive.serial_number))
      self.ui.drive_label.repaint()

      if self.ui.configframelabel.text() == "Axis 1":
         self.axis = self.drive.axis1

      else:
         self.axis = self.drive.axis0

   #*** OdriveToolGui.axisSave *****************************

   def checkerrors(self):
      dErrors = {}
      cAxis = self.ui.configframelabel.text()
      
      if self.axis.error:
         dErrors[cAxis] = [self.dAxisError[self.axis.error], {}]
         print(self.dAxisError[self.axis.error])

         if self.axis.motor.error:
            dErrors[cAxis][1]["motor"] = \
                  self.MotorError[self.axis.motor.error]

         if self.axis.controller.error:
            dErrors[cAxis][1]["controller"] = \
                  self.ControllerError[self.axis.controller.error]

         if self.axis.encoder.error:
            dErrors[cAxis][1]["encoder"] = \
                  self.EncoderError[self.axis.encoder.error]

      return dErrors

   #*** OdriveToolGui.checkerrors **************************
#*** class OdriveToolGui ***************************************************

def getenums():
   #print(dir(odrive.enums))

   aRay = dir(odrive.enums)

   dEnums = {}
   i = 0

   while not "__" in aRay[i]:
      dEnums[str(aRay[i])] = eval("odrive.enums.{}".format(aRay[i]))
      i = i+1

   #print(len(dEnums), dEnums, "\n")

   err = odrive.enums.errors.axis()
   aRay = dir(err)

   dAxisError = {}
   i = 0

   while not "__" in aRay[i]:
      dAxisError[eval("err.{}".format(aRay[i]))] = str(aRay[i])
      i +=1

   #print(dAxisError, "\n")

   err = odrive.enums.errors.motor()
   aRay = dir(err)

   dMotorError = {}
   i = 0

   while not "__" in aRay[i]:
      dMotorError[eval("err.{}".format(aRay[i]))] = str(aRay[i])
      i +=1

   #print(dMotorError, "\n")

   err = odrive.enums.errors.encoder()
   aRay = dir(err)

   dEncoderError = {}
   i = 0

   while not "__" in aRay[i]:
      dEncoderError[eval("err.{}".format(aRay[i]))] = str(aRay[i])
      i +=1

   #print(dEncoderError, "\n")

   err = odrive.enums.errors.controller()
   aRay = dir(err)

   dControllerError = {}
   i = 0

   while not "__" in aRay[i]:
      dControllerError[eval("err.{}".format(aRay[i]))] = str(aRay[i])
      i +=1

   #print(dControllerError, "\n")

   return (dEnums, dAxisError, dMotorError, dEncoderError, dControllerError)

#*** getenums **************************************************************

if __name__ == "__main__":
   OdriveToolGui()

