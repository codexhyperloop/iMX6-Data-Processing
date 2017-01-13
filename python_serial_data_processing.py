
'''
    Created for Team Codex Hyperloop pod
    Primarily edited by Codi West
    1-10-17
'''

import serial
import time

ser = serial.Serial(
    port='/dev/ttyACM0',    # Port for Raspberry Pi
    # port='dev/tty6',      # Port for UDOO
    baudrate=115200,
    parity='N',
    #stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
    )

#ser.flushOutput()
if  ser.isOpen():
    print 'Serial connected'

#i = 0
while (ser.inWaiting != 0):
    bytesToRead = ser.inWaiting()
    #read = ser.read(bytesToRead)
    read = ser.read(size=1)

    #i = int(read,16)
    #ser.write(read)
    #read1 = ser.read()
    if read==0x2C:
        print('\n')
    print([read])

    #print int("a",16)

    #i=i+1
    
    #print str(i)
    #ser.write()


