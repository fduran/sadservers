# "Jakarta": it's always DNS.

## Description

Can't <kbd>ping google.com</kbd>. It returns <kbd>ping: google.com: Name or service not known</kbd>. Expected is being able to resolve the hostname. (Note: currently the VMs can't ping outside so there's no automated check for the solution).

## Test

<kbd>ping -c 1 -q google.com |grep packets| cut -d',' -f2,3</kbd> should return <kbd>1 received, 0% packet loss</kbd><br>
<kbd>ping google.com</kbd> should return something like <kbd>PING google.com (172.217.2.46) 56(84) bytes of data.</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(curl -Is -m 2 google.com |head -1)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "HTTP/1.1 301 Moved Permanently" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b> No clues ¯\_(ツ)_/¯<br><br>(Open window once more to see the complete solution).<br><br>
<b>Solution: </b> a) Edit <i>/etc/nsswitch.conf</i> and add <i>dns</i> to the <i>hosts:</i> line after <i>files</i>.<br>