from __future__ import print_function
from re import match
import odrive
from odrive.utils import start_liveplotter
from enums import *
import time
import math
import sys
global M0current
global CollisionPosition1
global CollisionPosition2
global Vel1
global Iq1
global repeat
global key

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
#odrv0 = odrive.find_any(serial_number=serial1)
odrv0 = odrive.find_any()
print("odrive found!!!")

def liveplot():
    start_liveplotter(lambda: [
    odrv0.axis0.motor.current_control.Iq_measured])

liveplot()

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.trap_traj.config.vel_limit = 5
odrv0.axis0.controller.move_incremental(100, False)
Pos1 = odrv0.axis0.encoder.pos_estimate                
while True:
        M0current = odrv0.axis0.motor.current_control.Iq_measured
        CollisionPosition1 = odrv0.axis0.encoder.pos_estimate
        Iq1 = odrv0.axis0.motor.current_control.Iq_setpoint
        Vel1 = odrv0.axis0.encoder.vel_estimate
        #Pos2 = odrv0.axis0.encoder.pos_estimate
        #print("Vel " + str(odrv0.axis0.encoder.vel_estimate))
        print("Vel " + '{:.2f}'.format(Vel1))
        print("Motor Iq " + '{:.2f}'.format(Iq1))
        print("Position " + '{:.2f}'.format(CollisionPosition1))
        if (M0current > 3):
                odrv0.axis0.requested_state = AXIS_STATE_IDLE
                print("Motor Current " + '{:.2f}'.format(M0current))
                print("Motor Stop Position1 " + '{:.2f}'.format(CollisionPosition1))
                print("Motor Idle")
                #time.sleep(1)
                odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv0.axis0.controller.input_pos = CollisionPosition1 - 1
                time.sleep(0.2)
                #odrv0.axis0.requested_state = AXIS_STATE_IDLE
                break
#odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.move_incremental(-100, False)
time.sleep(0.1)
while True:
        M0current = odrv0.axis0.motor.current_control.Iq_measured
        CollisionPosition2 = odrv0.axis0.encoder.pos_estimate
        Iq1 = odrv0.axis0.motor.current_control.Iq_setpoint
        Vel1 = odrv0.axis0.encoder.vel_estimate
        print("Vel " + '{:.2f}'.format(Vel1))
        print("Motor Iq " + '{:.2f}'.format(Iq1))
        print("Position " + '{:.2f}'.format(CollisionPosition2))
        #print("Motor Current " + str(M0current))
        if (M0current < -3):
                odrv0.axis0.requested_state = 1
                print("Motor Current " + '{:.2f}'.format(M0current))
                print("Motor Stop Position2 " + '{:.2f}'.format(CollisionPosition2))
                print("Motor Idle")
                #time.sleep(1)
                odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv0.axis0.controller.input_pos = CollisionPosition2 + 1
                time.sleep(0.2)
                break
odrv0.axis0.trap_traj.config.vel_limit = 30
odrv0.axis0.controller.input_pos = CollisionPosition1 - 1
while (odrv0.axis0.encoder.pos_estimate < CollisionPosition1 - 1):
        if (odrv0.axis0.motor.current_control.Iq_measured > 4):
                print("Collision")
                odrv0.axis0.requested_state = AXIS_STATE_IDLE
                while odrv0.axis0.current_state != AXIS_STATE_IDLE:
                        time.sleep(0.1)
                odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv0.axis0.controller.input_pos = CollisionPosition2 - 1
                odrv0.axis0.requested_state = AXIS_STATE_IDLE
                while odrv0.axis0.current_state != AXIS_STATE_IDLE:
                        time.sleep(0.1)
                break
        pass
print("Axis0 Range  " + '{:.2f}'.format(CollisionPosition1 - CollisionPosition2))
odrv0.axis0.requested_state = AXIS_STATE_IDLE

while True:
        key = input ("Select Option ")
        if key == "y":
                print("Yes")
                break
        elif key == "n":
                print("NO")
                break

        
#odrv0.axis0.controller.input_pos = CollisionPosition2 + 1
#while (odrv0.axis0.encoder.pos_estimate > CollisionPosition2 + 1):
#        pass
#odrv0.axis0.controller.move_incremental(-40, False)


#odrv0.axis0.controller.input_pos = CollisionPosition1 - 1
#while (odrv0.axis0.encoder.pos_estimate < CollisionPosition1 - 1):
#        pass
#odrv0.axis0.controller.input_pos = CollisionPosition2 + 1
#while (odrv0.axis0.encoder.pos_estimate > CollisionPosition2 + 1):
#        pass
#odrv0.axis0.controller.input_pos = CollisionPosition1 - 1
#while (odrv0.axis0.encoder.pos_estimate < CollisionPosition1 - 1):
#        pass
#odrv0.axis0.controller.input_pos = CollisionPosition2 + 1
#while (odrv0.axis0.encoder.pos_estimate > CollisionPosition2 + 1):
#        pass

repeat = input ("Repeat?(Y/N)")
sys.exit()
