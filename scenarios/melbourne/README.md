# "Melbourne": WSGI with Gunicorn

## Description

There is a Python <a href="https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface">WSGI</a> web application file at <i>/home/admin/wsgi.py</i> , the purpose of which is to serve the string "Hello, world!". This file is served by a <a href="https://docs.gunicorn.org/en/stable/">Gunicorn</a> server which is fronted by an nginx server (both servers managed by systemd). So the flow of an HTTP request is: Web Client (curl) -> Nginx -> Gunicorn -> wsgi.py . The objective is to be able to curl the localhost (on default port :80) and get back "Hello, world!", using the current setup.

## Test

<kbd>curl -s http://localhost</kbd> returns <kbd>Hello, world!</kbd> (serving the wsgi.py file via Gunicorn and Nginx)

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(curl -s --unix-socket /run/gunicorn.sock http://localhost)
res=$(echo $res|tr -d '\r')

if [[ "$res" != "Hello, world!" ]]
then
  echo -n "NO"
  exit
fi

res=$(curl -s http://localhost)
res=$(echo $res|tr -d '\r')
if [[ "$res" = "Hello, world!" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Nginx is not running, start it and then try: <kbd>curl http://localhost</kbd> , which gives <i>502 Bad Gateway</i> error.<br><br>

<b>2. </b>in <kbd>cat /etc/nginx/sites-enabled/default</kbd> realize the file <i>/run/gunicorn.socket</i> does not exist. From <kbd>/etc/systemd/system/gunicorn.service</kbd> or <kbd>ps auxf|grep gunicorn</kbd> we see gunicorn is using the file <i>/run/gunicorn.sock</i> instead. Fix the nginx config file and restart nginx.<br><br>

<b>3. </b>Now <kbd>curl localhost</kbd> returns nothing and <kbd>curl -I localhost</kbd> works. We can also curl against the socket file: <kbd>curl --unix-socket /run/gunicorn.sock http://localhost</kbd> also returns nothing but <kbd>curl -I --unix-socket /run/gunicorn.sock http://localhost</kbd> works. (Next "clue" gives the solution).<br><br>

<b>Solution </b>From last command we see <i>Content-Length: 0</i>, fix the <i>wsgi.py</i> file (for ex use a number of bytes equal or greater than the 13 needed for the message, or take out the Content-Length header altogether) and restart the gunicorn service.