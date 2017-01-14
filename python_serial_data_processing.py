
'''
    Created for Team Codex Hyperloop pod
    Primarily edited by Codi West
    1-10-17
'''

import serial
import time
import struct
import array

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
    # print "Locating start bit"
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
            print '\nX = '
            print "Byte Array = %s" % ([accelX])
            accelX_Hex = accelX.encode("hex")
            print "Hex Value = %s" % accelX_Hex
            accelX_Int = int(accelX_Hex, 16)
            print "Integer Value = %s" % accelX_Int
            #
            print '\nY = '
            # print ([accelY])
            print "Byte Array = %s" % ([accelY])
            accelY_Hex = accelY.encode("hex")
            print "Hex Value = %s" % accelY_Hex
            accelY_Int = int(accelY_Hex, 16)
            print "Integer Value = %s" % accelY_Int
            #
            print '\nZ = '
            # print ([accelZ])
            print "Byte Array = %s" % ([accelZ])
            accelZ_Hex = accelZ.encode("hex")
            print "Hex Value = %s" % accelZ_Hex
            accelZ_Int = int(accelZ_Hex, 16)
            print "Integer Value = %s" % accelZ_Int
        ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        print '\n'

