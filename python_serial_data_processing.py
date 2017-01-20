#! /usr/bin/python
'''
    Created for Team Codex Hyperloop pod
    Original code by Codi West
    Created 1-10-17
    Version P-0.5
'''

import serial
#import time
import datetime
#import struct
#import array
#import io
import threading    # NOT Optimized YET
import logging      # To be utilized
import json

import random       # Used only for JSON testing

'''
try:
    import simplejson
except ImportError:
    import json
    # print ("simplejson import error")
'''

'''***************************************************************'''
''' Enable Logging '''

logging.basicConfig(filename='logdata.log',format='%(asctime)s: %(levelname)s: %(message)s',level=logging.DEBUG)

logging.info('Starting Python Program')


'''***************************************************************'''
''' Declare all variables - Decided to use globals '''

# Serial Connections
serUp = False
ser1Up = False
ser2Up = False


accelX = ''
accelY = ''
accelZ = ''

'''
accelX_Hex = ''
accelY_Hex = ''
accelZ_Hex = ''

accelX_Int = 1
accelY_Int = 1
accelZ_Int = 1
'''

'''***************************************************************'''


'''***************************************************************'''
''' Start all Serial connections (on start) '''
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
        #global serUp
        serUp = True
    else:
        print "WARNING: Primary SAM3X8E Processor Serial Disconnected"
        #global serUp
        serUp = False
except:
    print "WARNING: Primary SAM3X8E Processor Serial FATAL Failure"


''' Initialize Serial Connection to Auxiliary iMX6 Procesor '''
try:
    ser1 = serial.Serial(
        port='/dev/ttyAMA0',    # Port for Raspberry Pi -> Second Pi
        #port='dev/tty6',      # Port for UDOO
        baudrate=115200,
        parity='N',
        #stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
        )

    if  ser1.isOpen():
        print 'Auxiliary iMX6 Serial Connected'
        #global ser1Up
        ser1Up = True
    else:
        print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
        #global ser1Up
        ser1Up = False
except:
    print "WARNING: Auxiliary iMX6 Processor Serial FATAL Failure"


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
        #global ser2Up
        ser2Up = True
    else:
        print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"
        #global ser2Up
        ser2Up = False
except:
    print "WARNING: Auxiliary SAM3X8E Processor Serial FATAL Failure"

    

''' Declare all functions '''

#Check Serial Status
def checkSerial( ):
    # Serial
    global serUp
    try:
        if  ser.isOpen():
            # print 'Primary SAM3X8E Serial Connected'
            # global serUp
            serUp = True
        else:
            # print "WARNING: Primary SAM3X8E Processor Serial Disconnected"
            #global serUp
            serUp = False
    except:
        serUp = False
    # Serial 1
    global ser1Up
    if  ser1.isOpen():
        # print 'Auxiliary iMX6 Serial Connected'
        # global ser1Up
        ser1Up = True
        #print "it works"
        ser1.write('hello')
        r = ser1.read()
        print r
    else:
        # print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
        # global ser1Up
        ser1Up = False
    # Serial 2
    global ser2Up
    if  ser2.isOpen():
        # print 'Auxiliary SAM3X8E Serial Connected'
        # global ser2Up
        ser2Up = True
    else:
        # print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"
        # global ser2Up
        ser2Up = False


''' Works '''
# Conversion function from serial string to int (Complete)
def toInt( valStr ):
    valHex = valStr.encode("hex")
    valInt = int(valHex, 16)
    return valInt


# Print Acceleration Values (Needs more data from Brandon)
def printAccel():
    global accelX
    global accelY
    global accelZ
    print '\nX = '
    print "Byte Array = %s" % ([accelX])
    accelX_Hex = accelX.encode("hex")
    print "Hex Value = %s" % accelX_Hex
    accelX_Int = int(accelX_Hex, 16)
    #accelX_Int = toInt(accelX)
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


''' NOT COMPLETE '''
# Conversion of Two's Complement (Need info from Brandon)
'''
def twoConvert ( int )
    value = functionOf(int)
    return value

'''

# Read from a text file from webserver
def getCommand( ):
    try:
        file = open('web/command.txt', 'r')
        # print file.read()
        command = file.read()
        return command
    except:
        # print "File not found"
        logging.info('Command File NOT Found')
        

# Receive Current SAM Data through Serial (ser)
def getSer( ):
    global accelX
    global accelY
    global accelZ

    try:
        head = ""
        head = ser.read(1)
        # print ([head])    # Only needed for debugging
        if head == '\x01':
            integrity = False
            # print '\n'
            #print ('Start of sensor data')
            logging.info('Start of sensor data')
            #   Reads Accelerometer Sensor Data
            accelX = ser.read(2)
            accelY = ser.read(2)
            accelZ = ser.read(2)
            #   Tests End of Text (ETX)
            end = ser.read(2)
            #print ("Received data")
            logging.info('Primary Serial Data Received')
            # print ([end])
            if(end == '\x00\x03'):
                integrity = True
                # print 'Sensor Data Verified'
                logging.info('Sensor Data Verified')
                printAccel()
                jsonDump()
            else:
                # print "ALERT!!! Receive error from Primary SAM"
                logging.info('ALERT!!! Receive error from Primary SAM')
            # ser.read(1)         # The extra byte before 16BIT "head"
            # print integrity
            #print '\n'
    except:
        print "WARNING: Primary SAM3X8E Processor Serial FATAL Failure"
        logging.warning('WARNING: Primary SAM3X8E Processor Serial FATAL Failure')


''' NOT COMPLETE - Partial '''
# JSON Testing
# Declare dump all json function
def jsonDump( ):
    accelX_Int = toInt(accelX)
    accelY_Int = toInt(accelY)
    accelZ_Int = toInt(accelZ)
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
        'serialIMX2' : ser1.isOpen(),
        'serialSAM2' : ser2.isOpen()
        }
    with open('web/sam1data.json', mode='w') as f:
        json.dump(data, f)
    with open('web/datalog/sam1data%s.json' % time, mode='w') as f:
        json.dump(data, f)
    # print datetime.datetime.now().time()
    logging.info('JSON Successfully Dumped')


''' Temporary Functions '''
# Testing purposes
def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

# For testing Web Read of JSON
def randomjson( ):
    accelX_Int = random.random()
    accelY_Int = random.random()
    accelZ_Int = random.random()
    #
    time = str(datetime.datetime.now().time())
    data = {
        'timestamp' : time,
        'accelX' : accelX_Int,
        'accelY' : accelY_Int,
        'accelZ' : accelZ_Int,
        'calSpeed' : random.randint(0,1023943),
        'wheelSpeed' : random.randint(0,99923842),
        'position' : random.randint(0,1023943),
        'temp' : random.randint(0,1023943),
        'pressure' : random.uniform(0,20),
        'batVoltage' : random.uniform(0,20),
        'batCurrent' : random.uniform(0,20),
        'angularRateX' : random.uniform(0,20),
        'angularRateY' : random.uniform(0,20),
        'angularRateZ' : random.uniform(0,20),
        'attitudeX' : "hopeful",
        'attitudeY' : "enlightened",
        'attitudeZ' : "joyful",
        'dBrakePosition' : random.uniform(0,20),
        'dBrakeForce' : random.uniform(0,20),
        'magLevPosition' : random.uniform(0,20),
        'magBrakePosition' : random.uniform(0,20),
        'yawPosition' : random.uniform(0,20),
        'operationMode' : random.uniform(0,20),
        'systemErrors' : "All is according to plan (Not an actual value)",
        'systemAlerts' : "Ignorance is Bliss (Not an actual value)",
        'serialSAM1' : random.randint(0,1),
        'serialIMX2' : random.randint(0,1),
        'serialSAM2' : random.randint(0,1)
        }
    with open('web/sam1data.json', mode='w') as f:
        json.dump(data, f)
    with open('web/datalog/sam1data%s.json' % time, mode='w') as f:
        json.dump(data, f)
    # print datetime.datetime.now().time()
    logging.info('JSON Successfully Dumped')

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

'''
    Receive Start Command
    Receive Stop Command
    Receive Self Test Command
    Receive System Test Command
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
    command = getCommand()
    # Very dissapointed upon finding out Python does not have switch statements'
    if(command == 'stop'):
        # logging.warning('Received STOP command; Emergency Braking')
        checkSerial()
        # print 'stop'
    elif(command == 'start'):
        # logging.info('Received START command')
        checkSerial()
        # Send Start Command
        getSer()
        # printAccel()  # Contained in getSer()
        # jsonDump()    # Contained in getSer()
        # print 'start'
    elif(command == 'selftest'):
        # logging.info('Received SYSTEMTEST command')
        checkSerial()
        # print 'testing serial connections'
    elif(command == 'systemtest'):
        # logging.info('Received SELFTEST command')
        checkSerial()
        # print 'testing connections'
    elif(command == 'webtest'):
        randomjson()
    else:
        logging.info('Awaiting COMMAND: Running tests in the meantime')
        print "No command found"
        # checkSerial()
        # print 'Not receiving any commands from HQ'


        
    # Attempt multiple threads for separate serial connections - INCOMPLETE
    # Check Status of Serial Connections
        # Serial 0 (Primary SAM3X8E)
        # Serial 1 (Secondary iMX6)
        # Serial 2 (Secondary SAM3X8E)
    # Read file for external web command - INCOMPLETE
        # Send relay of command to external processors
            # Serial 0 (Primary SAM3X8E)
            # Serial 1 (Secondary iMX6)
            # Serial 2 (Secondary SAM3X8E)
    # Read incoming serial data
        # try Serial 0 (Primary SAM3X8E)
            # except switch to Serial 2 sensors
        # try Serial 1 (Secondary iMX6)
            # except print WARNING Secondary iMX not connected
        # try Serial 2 (Secondary SAM3X8E)
            #
    '''Reading SAM3X8E (Primary) serial - Create SEPARATE function'''

''' Legacy
    # print "Locating start bit"
    checkSerial()
    head = ""
    # head = ser.read(1)
    getSer()
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
        print ("Received data")
        # print ([end])
        if(end == '\x00\x03'):
            integrity = True
            print 'Sensor Data Verified'
            print accelX
            # printAccel(accelX, accelY, accelZ)
            jsonDump()
        else:
            print "ALERT!!! Receive error"
        # ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        print '\n'
'''

'''***************************************************************'''
''' Secondary UDOO LOOP - PSEUDOCODE '''
'''***************************************************************'''
'''
Check all serial connections
if Primary UDOO is running correctly
    Do nothing
else
    Take over role of Primary iMX6
        take over sensor readings
        print to webpage
        listen for commands
        etc

'''

