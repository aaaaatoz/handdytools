#!/usr/bin/python
import time
import re

#get the current DAY + HOURS
CurrentHours = time.strftime('%d/%m/%Y-%H',time.localtime(time.time()))
#define the search pattern
HourPattern = re.compile(CurrentHours)
TPMonPattern = re.compile(u'EXCEPTION-nswrta.corp.tpmon.http.TpmonInteraction-tr                                                                                  ansmitRequest-$')
JavaPattern = re.compile(u'^java.net.ConnectException: Connection refused$')
logfile = open('****file somewhere','r')
#log file
ErrorMsgFile = open('/tmp/oir.mon.log','a+')

while 1:
        #read the line from file
        line = logfile.readline()
        if not line:
                break
        # if not this hour, we will skip
        if not HourPattern.search(line) : continue
        if TPMonPattern.search(line):   #find the first line
                line = logfile.readline()
                if not line: break
                if JavaPattern.search(line):
                        print "find it"
                        ErrorMsgFile.write("OIR TPMON Timeout happens referring                                                                                   CHG1565870 - restart appserver may be required\n")
logfile.close()
ErrorMsgFile.close()
