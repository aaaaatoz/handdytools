#!/usr/bin/python
import re

#define the dictionaries by hours
Requests = dict((key, 0) for (key) in range(0,24))
Responses = dict((key, 0) for (key) in range(0,24))
Success = dict((key, 0) for (key) in range(0,24))
Verified = dict((key, 0) for (key) in range(0,24))
UnVerified = dict((key, 0) for (key) in range(0,24))
Failure = dict((key, 0) for (key) in range(0,24))
FailedWithNull = dict((key, 0) for (key) in range(0,24))
FailedWithError = dict((key, 0) for (key) in range(0,24))
Time = dict((key, []) for (key) in range(0,24))

#define the regular expression
RequestsString = re.compile("ValidationRequest")
ResponseString = re.compile("ValidationResponse")
SuccessString = re.compile("validationStatus=OK")
VerifiedString = re.compile("validationResult=VERIFIED")
unVerifiedString = re.compile("validationResult=NOT_VERIFIED")
FailureString = re.compile("validationStatus=ERROR")    #not used at the moment
FailedWithNullString = re.compile("validationResult=null")
FailedWithErrorString = re.compile("validationResult=SYSTEM_ERROR")

#define last transactions
lastReq = "NULL"
lastRes = "NULL"

#define some lambda function
maxTime = lambda x: 0 if len(x) == 0 else max(x)
minTime = lambda x: 0 if len(x) == 0 else min(x)
avgTime = lambda x: 0 if len(x) == 0 else sum(x)*1.0/len(x)
ratio = lambda x,y : "NA" if y ==0 else str("%.2f" %(x*100.0 /y))+"%"

for line in open("/usr/local/adm/intapps/certvalid/certvalid_audit.log","r"):
        if line[10:11] <> "-" : continue
        hour = int (line[11:13])
        timestamp = line[11:22]
        if RequestsString.search(line): # this is a request trace msg
                Requests[hour] += 1
                lastReq = timestamp
        else:                                                           # this is a response trace msg
                Responses[hour] += 1
                lastRes = timestamp
                if SuccessString.search(line):  # this response is success
                        Success[hour] += 1
                        if VerifiedString.search(line):
                                Verified[hour] += 1
                        if unVerifiedString.search(line):
                                UnVerified[hour] += 1
                        # to-do-list : calculate the time
                        #get the response time
                        line = line.strip().split()[-1][:-1]    #get time like requestTime=3424
                        time = int (line.split('=')[-1]) / 1000 #get seconds
                        Time[hour].append(time)
                if FailureString.search(line):  # this is a failure response trace msg
                        Failure[hour] += 1
                        if FailedWithNullString.search(line):
                                FailedWithNull[hour] += 1
                        if FailedWithErrorString.search(line):
                                FailedWithError[hour] += 1

#print the result
print "Certvalid Statistics for Today"
print "="*220
print "Hour:\tRequests\tResponses\tSuccess\t\tVerified\tNotVerified\tFailed\tFailedWithNull\tFailedWithError\t\tFailureRate\tMaxTime(s)\tMinTime(s)\tAveTime(s)"
for index in range(0,24):
        print "%d\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%s\t\t%d\t\t%d\t\t%.1f\t\t" %(index,Requests[index], Responses[index], Success[index], Verified[index],UnVerified[index],
                        Failure[index],FailedWithNull[index],FailedWithError[index],ratio(Failure[index],Requests[index]),maxTime(Time[index]),minTime(Time[index]),avgTime(Time[index]))


allReq = 0
for Request in Requests:
        allReq += (Requests[Request])
allSucc = 0
for success in Success :
        allSucc += (Success[success])
allFailed = 0
for fail in Failure:
        allFailed += Failure[fail]

#print the summary
print "\n" + "="*220
print "All Requests for the day:\t\t%d" %allReq
print "All Successful Response for the day:\t%d" %allSucc
print "All Failed Response for the day:\t%s" %allFailed
print "Failed Response Ratio for the day:\t%s" %ratio(allFailed,allReq)
print "Last Request:\t\t\t\t%s" %lastReq
print "Last Response:\t\t\t\t%s" %lastRes
