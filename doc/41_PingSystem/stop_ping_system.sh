#!/bin/bash

PID=`ps -ef | grep "start_ping_system.sh" | head -1 | awk '{ print $2 }'`

kill $PID

PID=`ps -ef | grep "python" | head -1 | awk '{ print $2 }'`
