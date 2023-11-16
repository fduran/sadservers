# "Cape Town": Nginx borked

## Description

There's an Nginx web server installed and managed by systemd. Running <kbd>curl -I 127.0.0.1:80</kbd> returns
<kbd>curl: (7) Failed to connect to localhost port 80: Connection refused</kbd> , fix it so when you curl you get the default Nginx page.

## Test

<kbd>curl -Is 127.0.0.1:80|head -1</kbd> returns <kbd>HTTP/1.1 200 OK</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(curl -Is 127.0.0.1:80|head -1)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "HTTP/1.1 200 OK" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1.</b> Check the status of Nginx: <kbd>systemctl status nginx</kbd><br><br>
<b>2.</b> Check Nginx configuration file with <kbd>nginx -t</kbd><br><br>
<b>3.</b> After fixing the Nginx config file at <kbd>/etc/nginx/sites-enabled/default</kbd> (deleting first character ;) and restarting Nginx, when you curl again you get a 500 HTTP error. Look at application error logs in <kbd>/var/log/ directory</kbd> for the cause.<br><br><br><br>(Open window once more to see the complete solution).<br><br>
<b>Solution:</b> (once previous steps done) As superuser, comment out or increase "LimitNOFILE" in <kbd>/etc/systemd/system/nginx.service</kbd> , reload the systemd configuration with <kbd>systemctl daemon-reload</kbd> and restart nginx with <kbd>systemctl restart nginx</kbd>