
'''
    Created for Team Codex Hyperloop pod
    Primarily edited by Codi West
    1-10-17
'''

import serial
import time
import struct

ser = serial.Serial(
    port='/dev/ttyACM0',    # Port for Raspberry Pi
    # port='dev/tty6',      # Port for UDOO
    baudrate=115200,
    parity='N',
    #stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
    )

if  ser.isOpen():
    print 'Serial connected'

# Must use with matching main.cpp in SAM3X8E-Libraries
while True:
    head = ser.read(1)
    # print ([head])    # Only needed for debugging
    if head == '\x01':  # SOH
        integrity = False
        print '\n'
        print ("Start of sensor data")
        #   Reads Accelerometer Sensor Data
        accelX = ser.read(2)
        accelY = ser.read(2)
        accelZ = ser.read(2)
        #   Tests End of Text (ETX)
        end = ser.read(2)
        # print ([end])
        if(end == '\x00\x03'):
            integrity = True
            print 'Sensor Data Verified'
            print 'X = '
            print ([accelX])
            print 'Y = '
            print ([accelY])
            print 'Z = '
            print ([accelZ])
        ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        print '\n'
