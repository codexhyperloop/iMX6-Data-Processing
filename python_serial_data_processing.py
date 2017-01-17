
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

'''***************************************************************'''
''' Start all Serial connections '''
'''***************************************************************'''
''' Initialize Serial Connection to Primary SAM3X8E Procesor '''
try:
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
        print 'Primary SAM3X8E Serial Connected'
    else:
        print "WARNING: Primary SAM3X8E Processor Serial Disconnected"
except:
    print "WARNING: Primary SAM3X8E Processor Serial Failure"


''' Initialize Serial Connection to Auxiliary iMX6 Procesor '''
try:
    ser1 = serial.Serial(
        # port='dev/tty6',      # Port for UDOO
        baudrate=115200,
        parity='N',
        #stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
        )

    if  ser1.isOpen():
        print 'Auxiliary iMX6 Serial Connected'
    else:
        print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
except:
    print "WARNING: Auxiliary iMX6 Processor Serial Failure"


''' Initialize Serial Connection to Auxiliary SAM3X8E Procesor '''
try:
    ser2 = serial.Serial(
        # port='dev/tty6',      # Port for UDOO
        baudrate=115200,
        parity='N',
        #stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
        )

    if  ser2.isOpen():
        print 'Auxiliary SAM3X8E Serial Connected'
    else:
        print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"
except:
    print "WARNING: Auxiliary SAM3X8E Processor Serial Failure"

    
'''***************************************************************'''
''' Declare all variables '''

'''
accelX = ''
accelY = ''
accelZ = ''

accelX_Hex = ''
accelY_Hex = ''
accelZ_Hex = ''

accelX_Int = 1
accelY_Int = 1
accelZ_Int = 1
'''

'''***************************************************************'''
''' Declare all functions '''

# Print Acceleration Values
def printAccel(accelX, accelY, accelZ):
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

''' Works '''
# Conversion function from serial string to int
def toInt( valStr ):
    valHex = valStr.encode("hex")
    valInt = int(valHex, 16)
    return valInt

''' NOT COMPLETE '''
# Conversion of Two's Complement
'''
def twoConvert ( int )
    value = functionOf(int)
    return value

'''

''' NOT COMPLETE - Partial '''
# JSON Testing
# Declare dump all json function
def jsonDump(accelX, accelY, accelZ):
    accelX_Int = toInt(accelX)
    accelY_Int = toInt(accelX)
    accelZ_Int = toInt(accelX)
    #
    time = str(datetime.datetime.now().time())
    data = {
        'timestamp' : time,
        'accelX' : accelX_Int,
        'accelY' : accelY_Int,
        'accelZ' : accelZ_Int,
        'calSpeed' : 0,
        'wheelSpeed' : 0,
        'position' : 0,
        'temp' : 0,
        'pressure' : 0,
        'batVoltage' : 0,
        'batCurrent' : 0,
        'angularRateX' : 0,
        'angularRateY' : 0,
        'angularRateZ' : 0,
        'attitudeX' : "hopeful",
        'attitudeY' : "enlightened",
        'attitudeZ' : "joyful",
        'dBrakePosition' : 0,
        'dBrakeForce' : 0,
        'magLevPosition' : 0,
        'magBrakePosition' : 0,
        'yawPosition' : 0,
        'operationMode' : 0,
        'systemErrors' : "All is according to plan (Not an actual value)",
        'systemAlerts' : "Ignorance is Bliss (Not an actual value)",
        'serialSAM1' : ser.isOpen(),
        'serialSAM2' : ser2.isOpen(),
        'serialIMX2' : ser1.isOpen()
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
Mag Brake Position
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
            print accelX
            printAccel(accelX, accelY, accelZ)
            jsonDump(accelX, accelY, accelZ)
        ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        print '\n'




