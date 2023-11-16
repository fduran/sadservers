# "Saskatoon": counting IPs.

## Description

There's a web server access log file at <kbd>/home/admin/access.log</kbd>. The file consists of one line per HTTP request, with the requester's IP address at the beginning of each line.
<br><br>Find what's the IP address that has the most requests in this file (there's no tie; the IP is unique). Write the solution into a file <kbd>/home/admin/highestip.txt</kbd>. For example, if your solution is "1.2.3.4", you can do <kbd>echo "1.2.3.4" > /home/admin/highestip.txt</kbd>

## Test

The SHA1 checksum of the IP address <kbd>sha1sum /home/admin/highestip.txt</kbd> is <kbd>6ef426c40652babc0d081d438b9f353709008e93</kbd> (just a way to verify the solution without giving it away.)

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(sha1sum /home/admin/highestip.txt |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "6ef426c40652babc0d081d438b9f353709008e93" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>To get the first field (IP) of the file, you can do <kbd>awk '{print $1}' access.log</kbd> or using "cut" with delimiter of space (-d' ') and picking the first field (-f1): <kbd>cat access.log |cut -d' ' -f1</kbd>. You may want to append a pipe <kbd> | head</kbd> or <kbd> | tail</kbd> as you construct the command to see how your filters are working.<br><br>

<b>2. </b>After the previous step, you want to sort the IPs so they are together and can be counted: <kbd>cat access.log | awk '{print $1}' |sort</kbd><br><br>

<b>3. </b>Now you want to do the count with "uniq -c", so we have so far: <kbd>awk '{print $1}' access.log |sort|uniq -c</kbd><br><br>

<b>4. </b>Finally you want to sort the results with "sort" (goes in ascending order) and get the latest one (with "tail -1"
 for example), or sort in reverse order with "sort -r" and get the top result:  <kbd>awk '{print $1}' access.log|sort|uniq -c|sort -r|head -1</kbd>. <br><br>(Open window once more to see the complete solution).<br><br>

<b>Solution:</b> One posible way is <kbd>awk '{print $1}' access.log|sort|uniq -c|sort -r|head -1|awk '{print $2}' > /home/admin/highestip.txt</kbd>