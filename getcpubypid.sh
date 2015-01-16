#get cpu usage by process-id as: GetCpu #pid#
function GetCpu
 {
 CpuValue=`ps -p $1 -o pcpu |grep -v CPU | awk '{print $1}' | awk -F. '{print $1}'`
 echo $CpuValue
 }
 
 #check if the process is over threshold
 function CheckCpu
 {
 PID=$1
 cpu=`GetCpu $PID`
 if [ $cpu -gt 80 ]
 then
 {
 echo “The usage of cpu is larger than 80%”
 }
 else
 {
 echo “The usage of cpu is normal”
 }
 fi
 }
