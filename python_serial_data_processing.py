
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
    if head == '\x01':
        integrity = False
        print '\n'
        print ("Start of sensor data")
        # print 'X = '
        accelX = ser.read(2)
        # print ([accelX])
        #
        # print 'newline ='
        newline = ser.read(2)   # Delimiter
        # print ([newline])
        #
        # print 'Y = '
        accelY = ser.read(2)
        # print ([accelY])
        #
        # print 'newline ='
        newline = ser.read(2)   # Delimiter
        # print ([newline])
        #
        # print 'Z = '
        accelZ = ser.read(2)
        # print ([accelZ])
        #
        # print 'newline ='
        newline = ser.read(2)   # Delimiter
        # print ([newline])
        #
        end = ser.read(2)
        # print ([end])
        if(end == '\x00\x03'):
            integrity = True
            print 'Sensor Data Verified'
            print '\nX = '
            print ([accelX])
            print '\nY = '
            print ([accelY])
            print '\nZ = '
            print ([accelZ])
        ser.read(1)         # The extra byte before 16BIT "head"
        # print integrity
        print '\n'


''' Deprecated code #2
# Must use with matching main.cpp in SAM3X8E-Libraries
while True:
    head = ser.read(1)
    # print ([head])    # Only needed for debugging
    if head == '\x01':
        integrity = False
        print '\n'
        print ("Start of sensor data")
        print 'X = '
        accelX = ser.read(2)
        print ([accelX])
        #
        print 'newline ='
        print ([ser.read(2)])
        #
        print 'Y = '
        accelY = ser.read(2)
        print ([accelY])
        #
        print 'newline ='
        print ([ser.read(2)])
        #
        print 'Z = '
        accelZ = ser.read(2)
        print ([accelZ])
        #
        print 'newline ='
        print ([ser.read(2)])
        #
        end = ser.read(2)
        print ([end])
        if(end == '\x00\x03'):
            integrity = True
            print 'Sensor Data Verified'
            #print accelX
            #print accelY
            #print accelZ
        ser.read(1)
        print integrity
        print '\n'
'''

''' Deprecated Code #1
#i = 0
while (ser.inWaiting != 0):
    bytesToRead = ser.inWaiting()
    #read = ser.read(bytesToRead)
    readByte = ser.read(1)
    #buf = struct.pack('%sf' % len(read), *read)
    #i = int(read,16)
    #ser.write(read)
    #read1 = ser.read()
    #result = bytearray.fromhex('read')
    #print result
    if readByte==0x2C:
        print('\n')
    print([readByte])

    #print int("a",16)

    #i=i+1
    
    #print str(i)
    #ser.write()
'''

