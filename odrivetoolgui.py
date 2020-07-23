import sys, time

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from ui_odrive import Ui_Odrive\

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
      print(self.drive.axis0.motor)
      print(dir(self.drive.axis0.motor))

   #*** OdriveToolGui.findanyodrive ************************

   def calibrateAxis0(self):

      self.ui.configframelabel.setText("Axis 0")
      self.axis = self.drive.axis0
      self.calibrateAxis()

   #*** OdriveToolGui.calibrateAxis0 ***********************

   def calibrateAxis1(self):

      self.ui.configframelabel.setText("Axis 1")
      self.axis = self.drive.axis1
      self.calibrateAxis(self.axis)

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
         
#*** class OdriveToolGui ***************************************************

if __name__ == "__main__":
   OdriveToolGui()

