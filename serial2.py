# make a while loop using this, checking "bytes received" as return value
# produces:
# serRXmsgType  (a char)
# serRXdata(typeFloat) or serRXdata(typeInt32)
# returns bytes successfully read in last go

def getSerial(ser): 										# use for all links
	try:
		RXwaiting=ser.inWaiting()							# ser.in_waiting() or ser.inWaiting() for amount in buffer
		if RXwaiting==0 or serDataRXtoTX==true:				# don't overwrite fresh data	
			return 0	
		else:
			if not serRXstatus<RXstarted:
				tmp=ser.read(1)
				if tmp<>startByte:							# scrap byte if startbyte not found
					serRXstatus=RXfailed
					serRXstep=0
					return 0
				else:	 									# begin a new frame if startbyte found
					serRXstatus=RXstarted
					serRXstep=1
					return 1	
			else:											# frame content parsed
				RXbytes=serProt(serRXstep)
				if RXwaiting<RXbytes:
					return 0
				else:										# parse if enough data arrived

					if serRXstep==1:
						serRXmsgType=ser.read(RXbytes)
						if serRXmsgType<192:				# at this time, only use msg 192-255
							serRXstatus=RXfailed							
							return 0
						else:
							serRXstep+=1
							return 1
							
					elif serRXstep==2:						# at this time, only using text data, 10 bytes
						serRXbuf=ser.read(RXbytes)
						if prmSize(serRXmsgType)>RXbytes:
							print 'Message '+serRXmsgType+': Truncated data of '+prmSize(serRXmsgType)+' to '+RXbytes+': '+tmp
						if prmForm(serRXmsgType) == typeFloat:
							serRXdata(typeFloat)=float(serRXbuf)
							serRXstep+=1							
						elif prmForm(serRXmsgType) == typeInt32:						
							serRXdata(typeInt32)=int(serRXbuf)
							serRXstep+=1
						else:
							print 'Message '+serRXmsgType+': data type unhandled'
							serRXstatus=RXfailed
							serRXstep=0
							return 0
						return RXbytes			
						
					elif serRXstep==3:
						serRXstopByte=ser.read(RXbytes)		# read stopbyte
						if serRXstopByte<>255:
							serRXstatus=RXfailed
							serRXstep=0
							return 0
						else:
							serRXstatus=RXfinished
							return 1
					else:
						serRXstatus=RXfailed
						return 0

	except:
		return 0





