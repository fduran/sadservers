# "Tokyo": can't serve web file

## Description

There's a web server serving a file <i>/var/www/html/index.html</i> with content "hello sadserver" but when we try to check it locally with an HTTP client like <kbd>curl 127.0.0.1:80</kbd>, nothing is returned. This scenario is not about the particular web server configuration and you only need to have general knowledge about how web servers work.

## Test

<kbd>curl 127.0.0.1:80</kbd> should return: <kbd>hello sadserver</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(curl -s -m 2 127.0.0.1:80)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "hello sadserver" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1.</b> Run the test. If "curl" doesn't return, perhaps something is blocking the network connection.<br><br>
<b>2.</b> Check the local firewall (iptables) settings with <kbd>iptables -L</kbd><br><br>
<b>3. Partial Solution:</b> Delete the iptables rule blocking port :80 , for example: <kbd>iptables -F</kbd> and test again.<br><br>
<b>4.</b> Check permissions and ownership of the index.html file with: <kbd>ls -l /var/www/html/index.html</kbd><br><br>
<b>5. Final solution:</b> change the ownership of the index file to the apache user: <kbd>chown www-data: /var/www/html/index.html</kbd> or allow other users to read the file owned by root (worse solution): <kbd>chmod 644 /var/www/html/index.html</kbd><br><br>