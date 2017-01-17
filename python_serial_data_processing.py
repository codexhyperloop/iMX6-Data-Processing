
'''
    Created for Team Codex Hyperloop pod
    Primarily edited by Codi West
    1-10-17
'''

import serial
import time
import datetime
import struct
import array
#import io

try:
    import simplejson
except ImportError:
    import json
    print ("simplejson import error")


''' Initialize Serial Connection to Connected SAM3X8E Procesor '''
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

''' Declare all variables '''
accelX = None
accelY = None
accelZ = None

accelX_Hex = None
accelY_Hex = None
accelZ_Hex = None

accelX_Int = None
accelY_Int = None
accelZ_Int = None

''' Declare all functions '''

# Print Acceleration Values
def printAccel():
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

# JSON Testing
# Declare dump all json function
def jsonDump():
    time = str(datetime.datetime.now().time())
    data = {
        'timestamp' : time,
        'accelX' : accelX_Int,
        'accelY' : accelY_Int,
        'accelZ' : accelZ_Int,
        'shares' : 108976,
        'Price' : 234
        }
    with open('sam1data.json', mode='w') as f:
        json.dump(data, f)
    with open('archive/sam1data%s.json' % time, mode='w') as f:
        json.dump(data, f)
    print datetime.datetime.now().time()


# Read all serial data function
''' Read All Data Function
MCU1 && CPU2 && MCU2
Acceleration (Gyroscope)
    X
    Y
    Z
Calculated Speed

Wheel Speed (Optosensor)

Position (Calculated)

Temperature

Pressure

Voltage

Current (Amp)


Disk Brake Position
Disk Brake Force
Mag Lev Position
Mag Brak Position
Yaw position



Time

'''

''' Dump JSON Data Function
Acceleration (Gyroscope)
    X
    Y
    Z
Calculated Speed

Wheel Speed (Optosensor)

Position (Calculated)

Temperature

Pressure

Voltage

Current (Amp)


Disk Brake Position
Disk Brake Force
Mag Lev Position
Mag Brak Position
Yaw position


Time
'''

''' Potentially Dump MySQL Data
'''

''' Receive Start Command

'''

''' Receive Stop Command

'''

''' Receive Self Test Command

'''

''' Receive System Test Command

'''

''' Check status of Other CPU and 2 MCUs

'''

''' Send Command to MCUs and failover CPU
switch:
    Wait is default
    Run Self Test
    Run Full System Test
    Start
    Emergency Stop
'''

'''***************************************************************'''
''' PRIMARY LOOP '''
'''***************************************************************'''
# Must use with matching main.cpp in SAM3X8E-Libraries
while True:
    # print "Locating start bit"
    head = ser.read(1)
    # print ([head])    # Only needed for debugging
    if head == '\x01':
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
            printAccel()
            jsonDump()
        ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        print '\n'




