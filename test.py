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


consoleBuffer = []

def consoleInput(myBuffer):
  while True:
    myBuffer.append(input())
 
threading.Thread(target=consoleInput, args=(consoleBuffer,)).start() # start the thread

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
#odrv0 = odrive.find_any(serial_number=serial1)
odrv0 = odrive.find_any()
print("odrive found!!!")

#def liveplot():
#    start_liveplotter(lambda: [
#            odrv0.axis0.encoder.pos_estimate])
    #odrv0.axis0.motor.current_control.Iq_measured])

#liveplot()

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.config.pos_gain = 10
odrv0.axis0.trap_traj.config.decel_limit = 200 
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
odrv0.axis0.trap_traj.config.vel_limit = 20
while True:
        #key = 0
        #while consoleBuffer:
        #        print(repr(consoleBuffer.pop(0)))
        #key = keyboard.read_key(True)
        #if consoleBuffer:
        #        print("Open Pressed")
                #keypress = repr(consoleBuffer.pop(0))
        if keyboard.is_pressed('o'):
                print("Open Pressed")
                odrv0.axis0.controller.input_pos = CollisionPosition1 - 2
                while (odrv0.axis0.encoder.pos_estimate < CollisionPosition1 - 2):
                        CurrentPosition = odrv0.axis0.encoder.pos_estimate
                        if (odrv0.axis0.motor.current_control.Iq_measured > 4):
                                print("Collision")
                                odrv0.axis0.controller.input_pos = CurrentPosition - 1
                                odrv0.axis0.requested_state = AXIS_STATE_IDLE
                                while (odrv0.axis0.current_state != AXIS_STATE_IDLE):
                                        time.sleep(0.1)
                                print("IDLE")
                                odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                                #odrv0.axis0.controller.input_pos = CurrentPosition - 1
                                print("CLOSE LOOP")
                                time.sleep(0.1)
                                odrv0.axis0.controller.input_pos = CollisionPosition2 + 1
                                while ( CurrentPosition > CollisionPosition2 + 1):
                                        time.sleep(0.1)
                                        CurrentPosition = odrv0.axis0.encoder.pos_estimate
                                print("HOME")
                                odrv0.axis0.requested_state = AXIS_STATE_IDLE
                                while (odrv0.axis0.current_state != AXIS_STATE_IDLE):
                                        time.sleep(0.1)
                                print("IDLE")
                                break
                        if keyboard.is_pressed('c'): keyboard.release
                                print("c Pressed")
                                CurrentPosition = odrv0.axis0.encoder.pos_estimate
                                odrv0.axis0.controller.input_vel = 0
                                odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                                odrv0.axis0.controller.input_vel = 0
                                print("Control Mode " + '{:.2f}'.format(odrv0.axis0.controller.config.control_mode))
                                #time.sleep(0.1)

                                #odrv0.axis0.requested_state = AXIS_STATE_IDLE
                                #while (odrv0.axis0.current_state != AXIS_STATE_IDLE):
                                #            time.sleep(0.05)
                                #odrv0.axis0.controller.input_pos = CurrentPosition
                                #odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                                #odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                                #time.sleep(.1)
                                #odrv0.axis0.controller.input_pos = CurrentPosition
                                #time.sleep(.1)
                                #time.sleep(0.1)
                                odrv0.axis0.controller.input_pos = CollisionPosition2 + 1
                                CurrentPosition = odrv0.axis0.encoder.pos_estimate
                                while (CurrentPosition > CollisionPosition2 + 1):
                                        time.sleep(0.1)
                                        CurrentPosition = odrv0.axis0.encoder.pos_estimate
                                break
        elif keyboard.is_pressed('c'):
                print("Close Pressed")
                odrv0.axis0.controller.input_pos = CollisionPosition2 + 1

print("Axis0 Range  " + '{:.2f}'.format(CollisionPosition1 - CollisionPosition2))
odrv0.axis0.requested_state = AXIS_STATE_IDLE
sys.exit()
