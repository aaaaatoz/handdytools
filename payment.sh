#$/usr/bin/bash
declare -a log
declare -a application
declare -a lastpayment

#parse the configuration file
index=1
echo "***************************************"
printf "Application\tLast Payment\n"
echo "***************************************"
while read line
do
        application[$index]=`awk 'NR=='$index' {print $1}' payment.conf`
        log[$index]=`awk 'NR=='$index' {print $2}' payment.conf`
        lastpayment[$index]=$(grep "FIN_RESP" ${log[$index]} | tail -1 | cut -c 1-23)
        printf "%-15s %-30s\n" ${application[$index]} ${lastpayment[$index]}
        let index=index+1
done < payment.conf
