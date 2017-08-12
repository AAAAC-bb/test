#!/bin/bash

for i in $(seq 1 30); do
    random_str=$1
    process_id=`ps -ef | grep $1 | egrep -v 'grep|sshpass|session_tracker' | awk '{print $2}'`
    echo $process_id
    if [ ! -z "$process_id" ];then
        echo "start run strace..."
        strace -fp $process_id -t -o ssh_audit_$2.log
        break;
    fi
    sleep 1
done
