#$/usr/bin/bash
declare -a log
declare -a application
declare -a lastpayment
declare -a lastpaymentsincenow

currentMin=$(date +%M | sed  's/^0//g')
currentHour=$(date +%H | sed  's/^0//g')

#parse the configuration file
index=1
echo "**************************************************************************"
printf "Application\tLast Payment\t\t\tSince now "
echo "(`date +%H:%M`)"
echo "**************************************************************************"
while read line
do
        application[$index]=`awk 'NR=='$index' {print $1}' payment.conf`
        log[$index]=`awk 'NR=='$index' {print $2}' payment.conf`
        lastpayment[$index]=$(grep "FIN_RESP" ${log[$index]} | tail -1 | cut -c 1-23)
        if [ -z "${lastpayment[$index]}" ]; then
                lastpayment[$index]="NULL"
                lastpaymentsincenow[$index]="NA"
        else
                lastpayhour=`expr ${lastpayment[$index]:11:2} + 0`
                lastpaymin=`expr ${lastpayment[$index]:14:2} + 0`
                let lastpaymentsincenow[$index]=($currentHour-$lastpayhour)*60+$currentMin-$lastpaymin
        fi
        printf "%-15s %-31s %-4s mins ago\n" ${application[$index]} ${lastpayment[$index]} ${lastpaymentsincenow[$index]}
        let index=index+1
done < payment.conf
