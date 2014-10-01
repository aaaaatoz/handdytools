#!/usr/bin/bash

#trunkate the file
cat /dev/null > pingresults-reachable.txt
cat /dev/null > pingresults-unreachable.txt

for server in `cat serverlist.txt`;
do
        ping $server 1 1 > /dev/null
        if [ $? = 0 ] ;
        then
                echo "$server is pingable" >> pingresults-reachable.txt
        else
                echo "$server is not pingable" >> pingresults-unreachable.txt
        fi
done
