#!/bin/bash
echo "The password should be 'calendall'"

ID="$(docker ps |grep calendall_web | awk '{print $1}')"
docker exec -it $ID pgcli -h calendall_db_1 -U calendall