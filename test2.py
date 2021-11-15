from __future__ import print_function
from re import match
import odrive
from odrive.utils import start_liveplotter
from enums import *
import time
import math
import sys
import keyboard
import threading
global M0current
global CollisionPosition1
global CollisionPosition2
global Vel1
global Iq1
global repeat
global keypressed
global CurrentPosition

print("finding an odrive...")
odrv0 = odrive.find_any()
print("odrive found!")
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
#odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
odrv0.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
odrv0.axis0.controller.config.vel_limit = 40
odrv0.axis0.encoder.config.bandwidth = 300
odrv0.axis0.trap_traj.config.decel_limit = 11   #11
odrv0.axis0.trap_traj.config.accel_limit = 60   #60
odrv0.axis0.trap_traj.config.vel_limit = 40     #40
odrv0.axis0.controller.input_pos = 0
 
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
while True:
        if keyboard.is_pressed('o'):
            print("Open Pressed")
            odrv0.axis0.controller.input_pos = 100
        if keyboard.is_pressed('c'):
            print("Close Pressed")
            odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
            odrv0.axis0.controller.input_pos = odrv0.axis0.encoder.pos_estimate
            time.sleep(0.5)
            odrv0.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
            odrv0.axis0.controller.input_pos = 0
        if keyboard.is_pressed('z'):
            print("Close2 Pressed")
            odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
            odrv0.axis0.controller.input_vel = 0
            #time.sleep(0.1)
            odrv0.axis0.controller.input_pos = 0
            odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
            odrv0.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
            #odrv0.axis0.controller.input_pos = 0
        if keyboard.is_pressed('r'):
            print("Reboot Pressed")
            odrv0.reboot()
                                
odrv0.axis0.requested_state = AXIS_STATE_IDLE
sys.exit()
