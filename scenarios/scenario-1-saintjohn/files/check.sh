#!/usr/bin/bash
res=$(find /var/log/bad.log -mmin -0.1)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "/var/log/bad.log" ]]
then
  echo -n "NO"
else
  echo -n "OK"
fi
