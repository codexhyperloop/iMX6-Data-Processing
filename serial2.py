#! /usr/bin/python

# make a while loop using this, checking "bytes received" as return value
# produces:
# serRXmsgType  (a char)
# serRXdata(typeFloat) or serRXdata(typeInt32)
# returns bytes successfully read in last go

import initdata1 as d

def getSerial(ser): 										# use for all links
#	try:
        #serProt[4]=0.123
        #print "SerProt=" + serProt[4]
        #print ser.inWaiting()
        RXwaiting=ser.inWaiting()							# ser.in_waiting() or ser.inWaiting() for amount in buffer
        #print RXwaiting
        if RXwaiting==0 or d.serDataRXtoTX==True:				# don't overwrite fresh data	
                return -1
        else:
                if d.serRXstatus<d.RXstarted:
                        tmp=ser.read(1)
                        print "start:"+tmp.encode("hex")
                        #print tmp+1
                        if tmp!=d.startByte:							# scrap byte if startbyte not found
                                d.serRXstatus=d.RXfailed
                                d.serRXstep=0
                                return -11
                        else:	 									# begin a new frame if startbyte found
                                d.serRXstatus=d.RXstarted
                                d.serRXstep=1
                                print "RECEIVING!"
                                return 1	
                else:											# frame content parsed
                        RXbytes=d.serProt[d.serRXstep]				
                        if RXwaiting<RXbytes:
                                return -12
                        else:										# parse if enough data arrived

                                if d.serRXstep==1:
                                        d.serRXmsgType=ord(ser.read())#RXbytes))
                                        print "msg: %i" % d.serRXmsgType #.encode("hex")
                                        if d.serRXmsgType<192:				# at this time, only use msg 192-255
                                                d.serRXstatus=d.RXfailed							
                                                return -13
                                        else:
                                                d.serRXstep+=1
                                                return 1
                                                
                                elif d.serRXstep==2:						# at this time, only using text data, 10 bytes
                                        serRXbuf=ser.read(RXbytes)
                                        print "data:"+serRXbuf.encode("hex")
                                        if d.prmSize[d.serRXmsgType]>RXbytes:
                                                print 'Message %i : Truncated data of %i to %i ' % (d.serRXmsgType, d.prmSize[d.serRXmsgType], RXbytes)
                                        if d.prmForm[d.serRXmsgType] == d.typeFloat:
                                                d.serRXdata[d.typeFloat]=float(serRXbuf)
                                                d.serRXstep+=1							
                                        elif d.prmForm[d.serRXmsgType] == d.typeInt32:						
                                                d.serRXdata[d.typeInt32]=int(serRXbuf.encode("hex"),16)
                                                d.serRXstep+=1
                                        else:
                                                print 'Message %i : data type unhandled' % d.serRXmsgType 
                                                d.serRXstatus=d.RXfailed
                                                d.serRXstep=0
                                                return -14
                                        return RXbytes			
                                        
                                elif d.serRXstep==3:
                                        serRXstopByte=ser.read(RXbytes)		# read stopbyte
                                        if serRXstopByte<>d.stopByte:
                                                d.serRXstatus=d.RXfailed
                                                d.serRXstep=0
                                                return -15
                                        else:
                                                d.serRXstatus=d.RXfinished
                                                d.serDataRXtoTX=True
                                                print "Finished!"
                                                return 1
                                else:
                                        d.serRXstatus=d.RXfailed
                                        return -16

#	except:
#		return 0





