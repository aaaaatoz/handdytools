#!/usr/bin/python
#ad-hoc script to test
'''this tool is going to do three things:
ping a server
create a socket
do http get / and record times
'''
import os
import re
import sys
import time
import socket
import urllib2

logfile = open("ccms.log","a")

ccmsstring = re.compile(r'ccms')

while True:
        time.sleep(10)
        currenttime = time.strftime('%H:%M:%S' ,time.localtime(time.time()))
        pingresult = os.system('ping localhost')
        if pingresult == 0 : #ping successful
                logfile.write(currenttime+ " "+ "ping ccms successfully\n")
		logfile.flush()
                #test port availablity
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
			t1 = time.time()
                        s.connect(("192.168.13.39",80))
			logfile.write(currenttime+ " "+ "open port 80 successfully\n")
			s.send("GET / HTTP/1.1\r\n\r\n")	#send the http GET REQUEST
			buf = None				#RESET THE buf value
			buf = s.recv(1000)
			t2 = time.time()
			if buf is None:
				logfile.write(currenttime+ " CCMS GET / testing failure"+ "\n")
			else:
				if ccmsstring.findall(buf) is not None:
					logfile.write(currenttime+ " CCMS GET / testing and found CCMS string in response within within %.3f seconds\n" %(t2-t1)) 
				else:
					logfile.write(currenttime+ " CCMS GET / testing but didn't find CCMS string in response"+ "\n")
                        s.close()
                except Exception,e:
                        continue
        else:
                logfile.write(currenttime+ " "+ "ping ccms failed\n")   #ping failed no need to test port and web
        logfile.flush()
