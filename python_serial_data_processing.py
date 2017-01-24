#! /usr/bin/python
'''
    Created for Team Codex Hyperloop pod
    Original code by Codi West
    Created 1-10-17
    Version P-0.65
'''

import serial
import time
import datetime
#import struct
#import array
#import io
import threading    # NOT Fully Optimized YET
import logging
import json

import random       # Used only for JSON testing

'''***************************************************************'''
''' Enable Logging '''

logging.basicConfig(filename='logdata.log',format='%(asctime)s: %(levelname)s: %(message)s',level=logging.DEBUG)

logging.info('Starting Python Program')


'''***************************************************************'''
''' Declare all variables - Decided to use globals '''

# Serial Connections
ser = ''
ser1 = ''
ser2 = ''


serUp = False
ser1Up = False
ser2Up = False

commandFlag = ''

# Sensor Data
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
''' Create Threading Class '''

class FuncThread(threading.Thread):
    def __init__(self, name, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        self.name = name
 
    def run(self):
        print "Starting " + self.name
        while True:
            self._target(*self._args)


        
'''***************************************************************'''
''' Declare all functions '''
'''***************************************************************'''

'''*********************************************'''
''' Start all Serial connections (Used in INIT) '''
# Initialize Serial Connection to Primary SAM3X8E Procesor
def initSer( ):
    global ser
    try:
        ser = serial.Serial(
            port='/dev/ttyACM0',    # Port for Raspberry Pi
            # port='dev/ttyS0',      # Port for UDOO (iMX6-1) -> Primary SAM
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

# Initialize Serial Connection to Auxiliary iMX6 Procesor
def initSer1( ):
    global ser1
    try:
        ser1 = serial.Serial(
            port='/dev/ttyAMA0',    # Port for Raspberry Pi -> Second Pi
            #port='dev/tty##',      # Port for UDOO (iMX6-1) -> Second iMX6
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


# Initialize Serial Connection to Auxiliary SAM3X8E Procesor
def initSer2( ):
    global ser2
    try:
        ser2 = serial.Serial(
            port='dev/ttySO',       # Port for Rasperry Pi -> Second SAM
            #port='dev/tty##',      # Port for UDOO (iMX6-1) -> Second SAM 
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


'''******************************************'''
''' Other Serial and Communication Functions '''
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
    try:
        if  ser1.isOpen():
            # print 'Auxiliary iMX6 Serial Connected'
            # global ser1Up
            ser1Up = True
            #r = ser1.read()
            #print r
        else:
            # print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
            # global ser1Up
            ser1Up = False
    except:
        ser1Up = False
        # print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
    # Serial 2
    global ser2Up
    try:
        if  ser2.isOpen():
            # print 'Auxiliary SAM3X8E Serial Connected'
            # global ser2Up
            ser2Up = True
        else:
            # print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"
            # global ser2Up
            ser2Up = False
    except:
        ser2Up = False
        # print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"


# INCOMPLETE
# Receive Current SAM1 Data through Serial (ser)
def readSer( ):
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
'''
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

# INCOMPLETE
# Send/Receive Commands to Secondary iMX6 through Serial (ser1)
def readSer1( ):

    try:
        head = ser1.read(1)
    except:
        print "WARNING: Primary SAM3X8E Processor Serial FATAL Failure"
        logging.warning('WARNING: Primary SAM3X8E Processor Serial FATAL Failure')


# INCOMPLETE
# Receive Current SAM2 Data through Serial (ser2)
def readSer2( ):

    try:
        head = ser12.read(1)
        if head == '\x01':
            # print '\n'
            #print ('Start of sensor data')
            logging.info('Start of sensor data')
        else:
            # print "ALERT!!! Receive error from Primary SAM"
            logging.info('ALERT!!! Receive error from Primary SAM')
        # ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        #print '\n'
    except:
        print "WARNING: Primary SAM3X8E Processor Serial FATAL Failure"
        logging.warning('WARNING: Primary SAM3X8E Processor Serial FATAL Failure')


# COMPLETE
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
        return "Error"


# INCOMPLETE
# Forward Command to SAM1, iMX2, and SAM2
'''
def sendCommand( ):
    try:
        
'''

'''*****************************'''
''' Data Manipulation Functions '''
# COMPLETE
# Conversion function from serial string to int (Complete)
def toInt( valStr ):
    valHex = valStr.encode("hex")
    valInt = int(valHex, 16)
    return valInt



# INCOMPLETE
# Conversion of Two's Complement (Need info from Brandon)
'''
def twoConvert ( int )
    value = functionOf(int)
    return value

'''



# PARTIALLY COMPLETE
# Dumps all current data to JSON files (1 current - others in /web/datalog)
def jsonDump( ):
    try:
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
        try:
            with open('web/datalog/sam1data%s.json' % time, mode='w') as f:
                json.dump(data, f)
            # print datetime.datetime.now().time()
            logging.info('JSON Successfully Dumped')
        except:
            os.mkdir('web/datalog/')
    except:
        logging.warning('FATAL: JSON Data Could Not Be Dumped')
        
'''
# Send current data to MySQL server for persistent storage - INCOMPLETE
def mysqlDump( ):
    
'''

'''***************************************************************'''
''' Temporary Functions - Working '''
'''***************************************************************'''
# Receive Current SAM Data through Serial (ser) --- For Testing purposes only
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


# Testing purposes
def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

# For testing Web Read of JSON
def randomjson( ):
    accelX_Int = random.random()
    accelY_Int = random.random()
    accelZ_Int = random.random()
    #
    timec = str(datetime.datetime.now().time())
    data = {
        'timestamp' : timec,
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
    time.sleep(0.2)

''' Read All Data Function
MCU1 && CPU2 && MCU2

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
''' INIT '''
'''***************************************************************'''
logging.info('Initializing...')
print 'Initializing...'

# Initialize Serial Connections for the first time
initSer()
initSer1()
initSer2()

# Create threads for continuous functions
checkSerThread = FuncThread("CheckSer-Thread", checkSerial)
dumpJSONThread = FuncThread("dumpJSON-Thread", jsonDump)

sendCommandThread = FuncThread("sendCommand-Thread", jsonDump)

RandomJSONThread = FuncThread("dumpJSON-Thread", randomjson)

'''***************************************************************'''
''' PRIMARY LOOP '''
'''***************************************************************'''
logging.info('Beginning Primary Loop')
print 'Beginning Primary Loop'

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
        # getSer()
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
        if RandomJSONThread.isAlive():
            # print "I am checking serial connections"
            thread1 = True
        else:
            RandomJSONThread.start()
        #print "Creating JSON files with RANDOM values"
    else:
        # logging.info('Awaiting COMMAND: Running tests in the meantime')
        # checkSerial()
        # print 'Not receiving any commands from HQ'
        if checkSerThread.isAlive():
            # print "I am checking serial connections"
            thread1 = True
        else:
            checkSerThread.start()
        


# TO DO
        
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
