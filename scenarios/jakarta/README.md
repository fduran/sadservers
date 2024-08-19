# "Jakarta": it's always DNS.

## Description

Can't <kbd>ping google.com</kbd>. It returns <kbd>ping: google.com: Name or service not known</kbd>. Expected is being able to resolve the hostname. (Note: currently, the VMs can't ping outside).

## Test

<kbd>ping google.com</kbd> should return something like <kbd>PING google.com (172.217.2.46) 56(84) bytes of data.</kbd>

<b>check.sh</b>

```bash
#!/usr/bin/bash

# Use getent to query the system's name resolution for google.com
res=$(getent hosts google.com)

if [[ -n "$res" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b> No clues ¯\_(ツ)_/¯<br><br>(Open window once more to see the complete solution).<br><br>
<b>Solution: </b> a) Edit <i>/etc/nsswitch.conf</i> and add <i>dns</i> to the <i>hosts:</i> line after <i>files</i>.<br>
