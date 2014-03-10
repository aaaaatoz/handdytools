import time
import socket
import urllib2

logfile = open("ccms.log","a")

while True:
	time.sleep(10)
	currenttime = time.strftime('%H:%M:%S' ,time.localtime(time.time()))
	pingresult = os.system('ping ccms')
	if pingresult == 0 : #ping successful
		logfile.write(currenttime+ " "+ "ping ccms successfully\n")
        #test port availablity
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect(("ccms",80))
			logfile.write(currenttime+ " "+ "open ccms tcp port 80 successfully\n")
			s.close()
            #test the url
			try:
				conn = urllib2.urlopen("http://ccms",timeout=10)
				httpCode = conn.getcode()
				logfile.write(currenttime+ " "+ "open ccms url successfully and the return code is %d\n" %httpCode)
				conn.close()
			except Exception,e:
				logfile.write(currenttime+ " "+ "open ccms url failed\n")
				continue
		except Exception,e:
			logfile.write(currenttime+ " "+ "open ccms tcp port 80 failed\n")
			continue
	else:
		logfile.write(currenttime+ " "+ "ping ccms failed\n")   #ping failed no need to test port and web
		logfile.flush()
