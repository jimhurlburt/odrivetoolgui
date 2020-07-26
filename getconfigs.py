#! /usr/bin/python3
""" gets config info for an axis and prints to file """

def getconfig(drive, axis, cAxis):
   dConfig = {}
   
   dConfig["vbus_voltage"] = drive.vbus_voltage
   dConfig["serial_number"] = drive.serial_number
   dConfig["fw_version_major"] = drive.fw_version_major
   dConfig["fw_version_minor"] = drive.fw_version_minor
   dConfig["fw_version_revision"] = drive.fw_version_revision

   dConfig["config"] = {"brake_resistance" :
                             drive.config.brake_resistance}

   dConfig[cAxis] = {"error" : axis.error}
   dConfig[cAxis]["motor"] = \
           {"error" : axis.motor.error}

   dConfig[cAxis]["motor"]["config"] = {}
   dTmp = dConfig[cAxis]["motor"]["config"]
   oTmp = axis.motor.config

   dTmp["pole_pairs"] = oTmp.pole_pairs

   dTmp["pre_calibrated"] = oTmp.pre_calibrated
   dTmp["calibration_current"] = oTmp.calibration_current
   dTmp["direction"] = oTmp.direction
   dTmp["motor_type"] = oTmp.motor_type
   dTmp["current_lim"] = oTmp.current_lim

   dConfig[cAxis]["controller"] = \
           {"error" : axis.controller.error}

   dConfig[cAxis]["controller"]["config"] = {}
   dTmp = dConfig[cAxis]["controller"]["config"]
   oTmp = axis.controller.config

   dTmp["control_mode"] = oTmp.control_mode
   dTmp["pos_gain"] = oTmp.pos_gain
   dTmp["vel_gain"] = oTmp.vel_gain
   dTmp["vel_integrator_gain"] = oTmp.vel_integrator_gain
   dTmp["vel_limit"] = oTmp.vel_limit
   dTmp["vel_ramp_rate"] = oTmp.vel_ramp_rate

   dConfig[cAxis]["encoder"] = \
           {"error" : axis.encoder.error}

   dConfig[cAxis]["encoder"]["config"] = {}
   dTmp = dConfig[cAxis]["encoder"]["config"]
   oTmp = axis.encoder.config

   dTmp["use_index"] = oTmp.use_index
   dTmp["pre_calibrated"] = oTmp.pre_calibrated
   dTmp["cpr"] = oTmp.cpr

   return dConfig

#*** getconfig *************************************************************

def showconfig(dConfig, cAxis):

   cFmt = "Odrive Serial# {0:x} -- Firmware {1:d}.{2:d}.{3:d}\n\n"
   cTxt = cFmt.format(dConfig["serial_number"],
                      dConfig["fw_version_major"],
                      dConfig["fw_version_minor"],
                      dConfig["fw_version_revision"])

   cTxt += "Bus Voltage: {:5.2f}\n".format(dConfig["vbus_voltage"])
   cTxt += "Config:\n   Brake resistance: {:4.2f}\n".\
              format(dConfig["config"]["brake_resistance"])

   cFmt = "\n{}:\n   error: {:d}\n"
   oAxis = eval("dConfig[\"{}\"]".format(cAxis))
   cTxt += cFmt.format(cAxis.capitalize(), oAxis["error"])

   oMotor = oAxis["motor"]
   cFmt = "\n   Motor:\n      error: {:d}\n\n"
   cTxt += cFmt.format(oMotor["error"])

   cTxt += " "*6 + "config:\n"
   cFmt = " "*9 + "pole_pairs: {:d}\n"
   cTxt += cFmt.format(oMotor["config"]["pole_pairs"])

   cFmt = " "*9 + "pre_calibrated: {}\n"
   cTxt += cFmt.format(oMotor["config"]["pre_calibrated"])

   cFmt = " "*9 + "calibration_current: {:4.1f}\n"
   cTxt += cFmt.format(oMotor["config"]["calibration_current"])

   cFmt = " "*9 + "direction: {:d}\n"
   cTxt += cFmt.format(oMotor["config"]["direction"])

   cFmt = " "*9 + "motor_type: {:d}\n"
   cTxt += cFmt.format(oMotor["config"]["motor_type"])

   cFmt = " "*9 + "current_lim: {:4.1f}\n"
   cTxt += cFmt.format(oMotor["config"]["current_lim"])

   oTmp = oAxis["controller"]
   cFmt = "\n   Controller:\n      error: {:d}\n\n"
   cTxt += cFmt.format(oTmp["error"])

   cTxt += " "*6 + "config:\n"
   cFmt = " "*9 + "pos_gain: {:2.2f}\n"
   cTxt += cFmt.format(oTmp["config"]["pos_gain"])

   cFmt = " "*9 + "vel_gain: {:6.4f}\n"
   cTxt += cFmt.format(oTmp["config"]["vel_gain"])

   cFmt = " "*9 + "vel_integrator_gain: {:6.4f}\n"
   cTxt += cFmt.format(oTmp["config"]["vel_integrator_gain"])

   cFmt = " "*9 + "vel_limit: {:6.0f}\n"
   cTxt += cFmt.format(oTmp["config"]["vel_limit"])

   cFmt = " "*9 + "vel_ramp_rate: {:6.0f}\n"
   cTxt += cFmt.format(oTmp["config"]["vel_ramp_rate"])

   #** encoder **************
   oTmp = oAxis["encoder"]
   cFmt = "\n   Encoder:\n      error: {:d}\n\n"
   cTxt += cFmt.format(oTmp["error"])

   cTxt += " "*6 + "config:\n"
   cFmt = " "*9 + "use_index: {}\n"
   cTxt += cFmt.format(oTmp["config"]["use_index"])

   cFmt = " "*9 + "pre_calibrated: {}\n"
   cTxt += cFmt.format(oTmp["config"]["pre_calibrated"])

   cFmt = " "*9 + "cpr: {:5.0f}\n"
   cTxt += cFmt.format(oTmp["config"]["cpr"])

   return cTxt

#*** showconfig ************************************************************

if __name__ == "__main__":
   import odrive

   # Find a connected ODrive (this will block until you connect one)
   print("finding an odrive...")
   drive = odrive.find_any()

   cAxis = "axis0"
   axis = drive.axis0
   dConfig = getconfig(drive, axis, cAxis)
   cTxt = showconfig(dConfig, cAxis)

   fh = open(cAxis + "_config.txt", 'wt')
   fh.write(cTxt)
   fh.close()
   
   print(cTxt)
