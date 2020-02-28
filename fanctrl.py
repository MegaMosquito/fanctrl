#
# Cooling fan control container
#
# Written by Glen Darling, February 2020.
#


import os
import subprocess
import threading
import time
import datetime



# Import the GPIO library so python can work with the GPIO pins
import RPi.GPIO as GPIO



# Debug flags
DEBUG_FAN = False

# Debug print
def debug(flag, str):
  if flag:
    print(str)




# These values need to be provided in the container environment
MY_FAN_CONTROL_PWM   = int(os.environ['MY_FAN_CONTROL_PWM'])



# Setup the GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MY_FAN_CONTROL_PWM, GPIO.OUT)
PWM_FREQUENCY = 110
fan_percent = GPIO.PWM(MY_FAN_CONTROL_PWM, PWM_FREQUENCY)



# Loop forever checking CPU temperature and adjusting the fan PWM
FAN_RAMP_START = 40.0 # I.e., fan starts to ramp up speed at this temp (in C)
FAN_RAMP_FULL = 60.0 # I.e., max fan starts at this temp (in C)
FAN_MIN = 25.0 # Baseline fan speed in percent (it will never go below this)
SLEEP_BETWEEN_TEMP_CHECKS_SEC = 20
CPUTEMP_PATH = '/cputemp'
class FanThread(threading.Thread):
  def run(self):
    global fan_percent
    debug(DEBUG_FAN, ("Fan management thread started!"))
    fn = CPUTEMP_PATH
    while True:
      with open(fn, 'r') as file:
        temp = float(file.read().replace('\n', '')) / 1000.0
      fan_ramp = 0
      if temp >= FAN_RAMP_START:
        fan_ramp = temp - FAN_RAMP_START
      if temp >= FAN_RAMP_FULL:
        fan_ramp = (FAN_RAMP_FULL - FAN_RAMP_START)
      fan_pct = int(100.0 * (fan_ramp / (FAN_RAMP_FULL - FAN_RAMP_START)))
      if fan_pct < FAN_MIN:
        fan_pct = FAN_MIN
      if fan_pct > 100:
        fan_pct = 100
      debug(DEBUG_FAN, ("--> FAN: t=%0.1f\N{DEGREE SIGN}C, f=%d%%\n" % (temp, fan_pct)))
      fan_percent.ChangeDutyCycle(fan_pct)
      time.sleep(SLEEP_BETWEEN_TEMP_CHECKS_SEC)



# Main program (instantiates and starts threads)
if __name__ == '__main__':

  # Fan: (set initial value; change with: `fan_percent.ChangeDutyCycle(100)`
  fan_percent.start(100)

  # Monitor CPU temperature and adjust fan accordingly
  fan = FanThread()
  fan.start()

  # Prevent exit
  while True:
    time.sleep(0.5)

