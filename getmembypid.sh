#get memory by pid as: GetMem #PID#
function GetMem
 {
 MEMUsage=`ps -o vsz -p $1|grep -v VSZ`
 (( MEMUsage /= 1000))
 echo $MEMUsage
 }
 
 mem=`GetMem $PID`
 if [ $mem -gt 1600 ]
 then
 {
 echo “The usage of memory is larger than 1.6G”
 }
 else
 {
 echo “The usage of memory is normal”
 }
 fi
