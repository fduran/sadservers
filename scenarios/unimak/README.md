# "Unimak Island": Fun with Mr Jason

## Description

Using the file <i>station_information.json</i> , find the station_id where "has_kiosk" is false  and "capacity" is greater than 30.
<br><br>
Save the station_id of the solution in the /home/admin/mysolution file, for example: <kbd>echo "ec040a94-4de7-4fb3-aea0-ec5892034a69" > ~/mysolution</kbd>
<br><br>
You can use the installed utilities <a href="https://jqlang.github.io/jq/" target="_new">jq</a>, <a href="https://github.com/tomnomnom/gron" target="_new">gron</a>, <a href="https://github.com/simeji/jid" target="_new">jid</a> as well as <a href="https://docs.python.org/3/library/json.html" target="_new">Python3</a> and <a href="https://gobyexample.com/json" target="_new">Golang</a>.

## Test

<kbd>md5sum /home/admin/mysolution</kbd> returns <kbd>8d8414808b15d55dad857fd5aeb2aebc</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(md5sum /home/admin/mysolution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "8d8414808b15d55dad857fd5aeb2aebc" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Use <kbd>jq</kbb> for example to inspect: <kbd>jq . station_information.json</kbd> then filter. (Next Clue will give the solution)<br><br>
<b>2. Solution.</b>For example: <kbd>jq '.data.stations[] | select(.has_kiosk==false and
 .capacity>30) | .station_id' station_information.json</kbd>
