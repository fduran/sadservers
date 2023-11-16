# "Taipei": Come a-knocking

## Description

There is a web server on port :80 protected with <a href="https://en.wikipedia.org/wiki/Port_knocking" target="_new">Port Knocking</a>. Find the one "knock" needed (sending a SYN to a single port, not a sequence) so you can <kbd>curl localhost</kbd>.

## Test

Executing <kbd>curl localhost</kbd> returns a message with md5sum <i>fe474f8e1c29e9f412ed3b726369ab65</i>.


<b>check.sh</b>

```
#!/bin/bash
res=$(curl -s localhost)
res=$(echo $res|tr -d '\r')
checksum=$(echo $res| md5sum| awk '{print $1}')

if [[ "$checksum" = "fe474f8e1c29e9f412ed3b726369ab65" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```


## Clues

<b>1. </b>You can use the <i>knock</i> utility, for example to knock on port 3000: <kbd>knock localhost 3000</kbd>. Netcat (nc) and nmap are also available. Note than nmap has some options where you'd need to be root (not possible here)<br><br>
<b>2. </b>You can also write a BASH script that knocks sequentially on all ports.<br><br>
<b>3. Solution.</b>Probably the fastest is using nmap against all ports, for example: <kbd>nmap -p- localhost</kbd>.