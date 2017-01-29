#! /usr/bin/python
'''
    Created for Team Codex Hyperloop pod
    Original code by Codi West
    Created 1-10-17
    Version P-0.8.0 (1/28/17)

    Can be compiled into C code through Cython (optionally have C datatypes added)
'''

import serial
import time
import datetime
#import struct
import array
#import io
import threading    # NOT Fully Optimized YET
#import multiprocessing
import logging
import json
import os
import string

import numpy

import random       # Used only for JSON testing

# See INIT Section for Nils's serial protocol
externalserial = False

'''***************************************************************'''
''' Enable Logging '''

logging.basicConfig(filename='logdata.log',format='%(asctime)s: %(levelname)s: %(message)s',level=logging.INFO)

logging.info('Starting Python Program')


'''***************************************************************'''
''' Switches whether or no to use Threading (for use with Cython) '''

threadingMode = False

'''***************************************************************'''
''' Declare all variables - Decided to use globals '''

# Serial Connections
serSAM1 = ''
serIMX2 = ''
serSAM2 = ''


serSAM1Up = False
serIMX2Up = False
serSAM2Up = False

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

# Sensor Data Arrays
#serProt=array.array('i',(0,)*5)
'''
serProt = numpy.zeros(shape=(5))
serRXdata = numpy.zeros(shape=(5))
serDataName = numpy.zeros(shape=(255))
prmForm = numpy.zeros(shape=(255))
prmSize = numpy.zeros(shape=(255))
'''

'''***************************************************************'''
''' Create Threading Class '''

class FuncThread(threading.Thread):
    def __init__(self, name, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        self.name = name
        self._pause = False # threading.Event()

    def pause(self):
        print "Pausing " + self.name
        logging.info("Pausing " + self.name)
        self._pause = True
        # print self._pause

    def resume(self):
        print "Restarting " + self.name
        logging.info("Restarting " + self.name)
        self._pause = False
        # print self._pause

    def paused(self):
        return self._pause  # .isSet()

    def run(self):
        print "Starting " + self.name
        while True:
            while not self._pause:
                self._target(*self._args)
            # print self.name + ' is paused'
            logging.debug(self.name + ' is paused')

'''***************************************************************'''
''' Create Multiprocessing Class  Canceled Testing '''
'''
class FuncProcess(multiprocessing.Process):
    def __init__(self, name, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        self.name = name
 
    def run(self):
        print "Starting " + self.name
        while True:
            self._target(*self._args)
'''   
'''***************************************************************'''
''' Declare all functions '''
'''***************************************************************'''

'''*********************************************'''
''' Start all Serial connections (Used in INIT) '''
# Initialize Serial Connection to Primary SAM3X8E Procesor
def initSerSAM1( ):
    global serSAM1
    try:
        serSAM1 = serial.Serial(
            port='/dev/ttyACM0',    # Port for Raspberry Pi
            # port='dev/ttyS0',      # Port for UDOO (iMX6-1) -> Primary SAM
            baudrate=115200,
            parity='N',
            #stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None
            )

        if  serSAM1.isOpen():
            print 'Primary SAM3X8E Serial Connected'
            #global serUp
            serSAM1Up = True
        else:
            print "WARNING: Primary SAM3X8E Processor Serial Disconnected"
            #global serUp
            serSAM1Up = False
    except:
        print "WARNING: Primary SAM3X8E Processor Serial FATAL Failure"

# Initialize Serial Connection to Auxiliary iMX6 Procesor
def initSerIMX2( ):
    global serIMX2
    try:
        serIMX2 = serial.Serial(
            port='/dev/ttyAMA0',    # Port for Raspberry Pi -> Second Pi
            #port='dev/tty##',      # Port for UDOO (iMX6-1) -> Second iMX6
            baudrate=115200,
            parity='N',
            #stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None
            )

        if  serIMX2.isOpen():
            print 'Auxiliary iMX6 Serial Connected'
            #global serIMX2Up
            serIMX2Up = True
        else:
            print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
            #global serIMX2Up
            serIMX2Up = False
    except:
        print "WARNING: Auxiliary iMX6 Processor Serial FATAL Failure"


# Initialize Serial Connection to Auxiliary SAM3X8E Procesor
def initSerSAM2( ):
    global serSAM2
    try:
        serSAM2 = serial.Serial(
            port='dev/ttySO',       # Port for Rasperry Pi -> Second SAM
            #port='dev/tty##',      # Port for UDOO (iMX6-1) -> Second SAM 
            baudrate=115200,
            parity='N',
            #stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None
            )

        if  serSAM2.isOpen():
            print 'Auxiliary SAM3X8E Serial Connected'
            #global serSAM2Up
            serSAM2Up = True
        else:
            print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"
            #global serSAM2Up
            serSAM2Up = False
    except:
        print "WARNING: Auxiliary SAM3X8E Processor Serial FATAL Failure"


'''******************************************'''
''' Other Serial and Communication Functions '''
#Check Serial Status (ALL)
def checkSerial( ):
    # Serial SAM1
    global serSAM1Up
    try:
        if  serSAM1.isOpen() and serSAM1.inWaiting():
            #print 'Primary SAM3X8E Serial Connected'
            serSAM1Up = True
        else:
            #print "WARNING: Primary SAM3X8E Processor Serial Disconnected"
            serSAM1Up = False
    except:
        serSAM1Up = False
        #print "FATAL: Primary SAM3X8E Serial Not Initialized"
        try:
            initSerSAM1()
        except:
            serSAM1Up = False
    # Serial IMX2
    global serIMX2Up
    try:
        if  serIMX2.isOpen() and serIMX2.inWaiting():
            #print 'Auxiliary iMX6 Serial Connected'
            serIMX2Up = True
        else:
            #print "WARNING: Auxiliary iMX6 Processor Serial Disconnected"
            serIMX2Up = False
    except:
        serIMX2Up = False
        #print "FATAL: Auxiliary iMX6 Processor Not Initialized"
        try:
            initSerIMX2()
        except:
            serIMX2Up = False
    # Serial SAM2
    global serSAM2Up
    try:
        if  serSAM2.isOpen() and serSAM2.inWaiting():
            #print 'Auxiliary SAM3X8E Serial Connected'
            serSAM2Up = True
        else:
            #print "WARNING: Auxiliary SAM3X8E Processor Serial Disconnected"
            serSAM2Up = False
    except:
        serSAM2Up = False
        #print "FATAL: Auxiliary SAM3X8E Processor Not Initialized"
        try:
            initSerSAM2()
        except:
            serSAM2Up = False


# COMPLETE
#Check Serial Status (ONLY SAM1)
def checkSerialSAM1( ):
    # Serial SAM1
    global serSAM1Up
    try:
        if  serSAM1.isOpen() and serSAM1.inWaiting():
            #print 'Primary SAM3X8E Serial Connected'
            serSAM1Up = True
        else:
            #print "WARNING: Primary SAM3X8E Processor Serial Disconnected"
            serSAM1Up = False
    except:
        serSAM1Up = False
        print "FATAL: Primary SAM3X8E Serial Not Initialized"
        try:
            initSerSAM1()
        except:
            serSAM1Up = False
            

# INCOMPLETE
# Receive Current SAM1 Data through Serial (serSAM1)
def readSerSAM1( ):
    global accelX
    global accelY
    global accelZ

    try:
        head = ""
        head = serSAM1.read(1)
        # print ([head])    # Only needed for debugging
        if head == '\x01':
            integrity = False
            # print '\n'
            #print ('Start of sensor data')
            logging.info('Start of sensor data')
            #   Reads Accelerometer Sensor Data
            accelX = serSAM1.read(2)
            accelY = serSAM1.read(2)
            accelZ = serSAM1.read(2)
            #   Tests End of Text (ETX)
            end = serSAM1.read(2)
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
            # serSAM1.read(1)         # The extra byte before 16BIT "head"
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
# Send/Receive Commands to Secondary iMX6 through Serial (serIMX2)
def readSerIMX2( ):

    try:
        head = serIMX2.read(1)
    except:
        print "WARNING: Secondary iMX6 Processor Serial FATAL Failure"
        logging.warning('WARNING: Secondary iMX6 Processor Serial FATAL Failure')


# INCOMPLETE
# Receive Current SAM2 Data through Serial (serSAM2)
def readSerSAM2( ):

    try:
        head = serSAM2.read(1)
        if head == '\x01':
            # print '\n'
            #print ('Start of sensor data')
            logging.info('Start of sensor data')
        else:
            # print "ALERT!!! Receive error from Primary SAM"
            logging.info('ALERT!!! Receive error from Secondary SAM')
        # ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        #print '\n'
    except:
        print "WARNING: Secondary SAM3X8E Processor Serial FATAL Failure"
        logging.warning('WARNING: Secondary SAM3X8E Processor Serial FATAL Failure')


# COMPLETE
# Read command from a text file on webserver
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

# COMPLETE
# Read threading option from a text file on webserver
def threadOption( ):
    try:
        file = open('web/threading.txt', 'r')
        # print file.read()
        threadingr = file.read()
        if threadingr == "true":
            return True
        elif threadingr == "false":
            return False            
    except:
        print "Threading Option: File Not Found"
        logging.info("Threading Option: File Not Found")
        return False


# INCOMPLETE
# Forward Command to SAM1, iMX2, and SAM2
'''
def sendCommandSAM1():
    try:
        if(command == 'emergencystop'):
            serSAM1.write() # 
        elif(command == 'start'):
            serSAM1.write() # 
        elif(command == 'stop'):
            serSAM1.write() # 
        elif(command == 'serialcheck'):
            serSAM1.write() # 
        elif(command == 'selftest'):
            serSAM1.write() # 
        elif(command == 'systemtest'):
            serSAM1.write() # 
        elif(command == 'webtest'):
            serSAM1.write() # 
        elif(command == 'systemexit'):
            serSAM1.write() # 
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
        accelX_Int = 0 #toInt(accelX)
        accelY_Int = 0 #toInt(accelY)
        accelZ_Int = 0 #toInt(accelZ)
        #
        timec = str(datetime.datetime.now().time())
        data = {
            'timestamp' : timec,
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
            'serialSAM1' : serSAM1Up,
            'serialIMX2' : serIMX2Up,
            'serialSAM2' : serSAM2Up,
            'receivedComand' : command
            }
        with open('web/sam1data.json', mode='w') as f:
            json.dump(data, f)
        try:
            with open('web/datalog/sam1data%s.json' % time, mode='w') as f:
                json.dump(data, f)
            # print datetime.datetime.now().time()
            logging.debug('JSON Successfully Dumped')
        except:
            os.mkdir('web/datalog/')
            print 'datalog folder created'
            logging.info('datalog folder created')
        time.sleep(0.2)
    except:
        logging.warning('FATAL: JSON Data Could Not Be Dumped')
        print 'FATAL: JSON Data Could Not Be Dumped'
        
'''
# Send current data to MySQL server for persistent storage - INCOMPLETE
def mysqlDump( ):
    
'''

'''***************************************************************'''
''' Temporary Functions - Working '''
'''***************************************************************'''
# Receive Current SAM Data through Serial (serSAM1) --- For Testing purposes only
def getSer( ):
    global accelX
    global accelY
    global accelZ

    try:
        head = ""
        head = serSAM1.read(1)
        # print ([head])    # Only needed for debugging
        if head == '\x01':
            integrity = False
            # print '\n'
            #print ('Start of sensor data')
            logging.info('Start of sensor data')
            #   Reads Accelerometer Sensor Data
            accelX = serSAM1.read(2)
            accelY = serSAM1.read(2)
            accelZ = serSAM1.read(2)
            #   Tests End of Text (ETX)
            end = serSAM1.read(2)
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
            # serSAM1.read(1)         # The extra byte before 16BIT "head"
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
    try:
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
            'calSpeed' : random.uniform(0,150),
            'wheelSpeed' : random.uniform(0,150),
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
            'serialSAM2' : random.randint(0,1),
            'receivedComand' : command
            }
        with open('web/sam1data.json', mode='w') as f:
            json.dump(data, f)
        try:
            with open('web/datalog/sam1data%s.json' % time, mode='w') as f:
                json.dump(data, f)
            # print datetime.datetime.now().time()
            logging.debug('JSON Successfully Dumped')
        except:
            os.mkdir('web/datalog/')
            print 'datalog folder created'
            logging.info('datalog folder created')
        time.sleep(0.2)
    except:
        logging.warning('FATAL: JSON Data Could Not Be Dumped')

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


# Imports from Nils
if True:
    #import initdata1
    import serial2

print serial2.d.serProt[0]

i=128
while (i<129):
    #print serial2.d.serDataName[i]
    i = i +1



# Initialize Serial Connections for the first time
initSerSAM1()
#initSerIMX2()
#initSerSAM2()


i=0
while i<100:
    head = serSAM1.read()
    print head.encode("hex")
    i=i+1


'''
i=0
j=0
while i<30 and j<100000:
    tmp=serial2.getSerial(serSAM1)
    if tmp>0:
        #print tmp
        i=i+1  # IN Java i++     
    j+=1
    serDataRXtoTX=False
    print tmp
'''

threadingMode = threadOption()

if threadingMode:
    print "Threading mode enabled"
    # Create threads for continuous functions
    checkSerThread = FuncThread("CheckSer-Thread", checkSerial)
    dumpJSONThread = FuncThread("dumpJSON-Thread", jsonDump)

    #relayCommandThread = FuncThread("relayCommand-Thread", relayCommand)

    RandomJSONThread = FuncThread("randomJSON-Thread", randomjson)

    # RandomJSONProcesss = FuncProcess("dumpJSON-Thread", randomjson)
else:
    print "Threading mode not enabled"

'''***************************************************************'''
''' PRIMARY LOOP '''
'''***************************************************************'''
logging.info('Beginning Primary Loop')
print 'Beginning Primary Loop'

# Must use with matching main.cpp in SAM3X8E-Libraries

# For THREADING = ENABLED (Highly Experimental)
if threadingMode:
    while True:
        command = getCommand()
        # Very dissapointed upon finding out Python does not have switch statements'
        if(command == 'stop'):
            # Pauses all threads
            if RandomJSONThread.isAlive():
                if not RandomJSONThread.paused():
                    RandomJSONThread.pause()
            #else:
                #print "randomJSON not alive"
            if checkSerThread.isAlive():
                if not checkSerThread.paused():
                    checkSerThread.pause()
            #else:
                #print "Serial Check not alive"
            if dumpJSONThread.isAlive():
                if not dumpJSONThread.paused():
                    dumpJSONThread.pause()
            #else:
                #print "dumpJSON not alive"
            # logging.warning('Received STOP command; Emergency Braking')
            # print 'stop'
        elif(command == 'start'):
            # Pauses unnecessary threads
            if RandomJSONThread.isAlive():
                if not RandomJSONThread.paused():
                    RandomJSONThread.pause()
            # Starts Needed Threads
            if dumpJSONThread.isAlive():
                thread1 = True
            else:
                dumpJSONThread.start()
            if dumpJSONThread.paused():
                dumpJSONThread.resume()
            # logging.info('Received START command')
            # Send Start Command
            # printAccel()  # Contained in getSer()
            # jsonDump()    # Contained in getSer()
            # print 'start'
        elif(command == 'selftest'):
            logging.debug('Received SYSTEMTEST command')
            # print 'testing serial connections'
        elif(command == 'systemtest'):
            logging.debug('Received SELFTEST command')
            # print 'testing connections'
        elif(command == 'webtest'):
            if RandomJSONThread.isAlive():
                thread1 = True
            else:
                RandomJSONThread.start()
            if RandomJSONThread.paused():
                RandomJSONThread.resume()
            #print "Creating JSON files with RANDOM values"
        elif(command == 'serialcheck'):       
            if checkSerThread.isAlive():
                # print "I am checking serial connections"
                thread1 = True
            else:
                checkSerThread.start()
            if checkSerThread.paused():
                checkSerThread.resume()
        elif(command == 'exitprogram'):
            exit()
        else:
            # logging.info('Awaiting COMMAND: Running tests in the meantime')
            # print 'Not receiving any commands from HQ'
            logging.debug('Not receiving any commands from HQ')


# For THREADING = DISABLED (Default)
'''
else:
    while True:
        command = getCommand()
        if(command == 'emergencystop'):
            checkSerialSAM1()       # Notifies SAM1 to Emergency Brake
            #sendCommandSAM1()
        elif(command == 'start'):
            checkSerialSAM1()
            #sendCommandSAM1()
            #readSerSAM1()
            jsonDump()
        elif(command == 'stop'):
            checkSerialSAM1()
            #sendCommandSAM1()
        elif(command == 'serialcheck'):
            checkSerialSAM1()
            #sendCommandSAM1()
        elif(command == 'selftest'):
            checkSerialSAM1()
            #sendCommandSAM1()
        elif(command == 'systemtest'):
            checkSerialSAM1()
            #sendCommandSAM1()
        elif(command == 'webtest'):
            #sendCommandSAM1()      # To notify SAM1 to hold tight
            randomjson()
        elif(command == 'exitprogram'):
            #sendCommandSAM1()      # To notify SAM1 to hold tight
            exit()
'''

# TO DO
        
# Attempt multiple threads for separate serial connections - COMPLETE
# Check Status of Serial Connections
    # Serial 0 (Primary SAM3X8E)
    # Serial 1 (Secondary iMX6)
    # Serial 2 (Secondary SAM3X8E)
# Read file for external web command - COMPLETE
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
if Primary UDOO is running correctly (receiving correct serial data)
    Do nothing
else
    Take over role of Primary iMX6
        take over sensor readings
        print to webpage
        listen for commands
        etc
'''
