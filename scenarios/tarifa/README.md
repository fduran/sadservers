# "Tarifa": Between Two Seas

## Description

There are three Docker containers defined in the <i>docker-compose.yml</i> file: an HAProxy accepting connetions on port :5000 of the host, and two nginx containers, not exposed to the host.<br><br>
The person who tried to set this up wanted to have HAProxy in front of the (backend or upstream) nginx containers load-balancing them but something is not working.

## Test

Running <kbd>curl localhost:5000</kbd> several times returns both <kbd>hello there from nginx_0</kbd> and <kbd>hello there from nginx_1</kbd><br><br>
Check <i>/home/admin/agent/check.sh</i> for the test that "Check My Solution" runs.  


<b>check.sh</b>

```
#!/bin/bash
# DO NOT MODIFY THIS FILE ("Check My Solution" will fail)

found=0

for i in {1..4}
do
  res=$(curl -s localhost:5000)
  ex=$?
  if test "$ex" != "0"; then
     echo -n "NO"
     exit
  fi

  res2=$(echo $res|grep -s nginx_0)
  ex=$?
  if test "$ex" != "0"; then
     continue
  else
    found=1
    break
  fi
done

if test "$found" != "1"; then
   echo -n "NO"
   exit
fi

for i in {1..4}
do
  res=$(curl -s localhost:5000)
  ex=$?
  if test "$ex" != "0"; then
     echo -n "NO"
     exit
  fi

  res2=$(echo $res|grep -s nginx_1)
  ex=$?
  if test "$ex" != "0"; then
     continue
  else
    echo -n "OK"
    exit
  fi
done

echo -n "NO"
```

## Clues

<b>1. </b>Run <kbd>curl localhost:5000</kbd> a few times to see we are only getting responses from one of the nginx servers. Checking the docker logs with: <kbd>docker compose logs</kbd> (or the log for each container with: <kbd>docker logs haproxy</kbd>) we see a message <i>could not resolve address 'nginx_1'</i> and no messages (UP or DOWN) about nginx_1<br><br>
<b>2. </b>The reason haproxy cannot resolve nginx_1 is because in the docker-compose.yml definition, nginx_1 uses the <i>backend_network</i> while haproxy and nginx_0 use <i>frontend_network</i>. To fix this we can have all 3 containers on the same network (deleting all network definitions and references) or adding <i>backend_network</i> as an haproxy <i>networks:</i> definition.<br>Restart Docker Compose with: <kbd>docker compose up -d --force-recreate</kbd> (a "restart" is not enough).<br><br> 
<b>3. </b>Now from <kbd>docker logs haproxy</kbd> the nginx_1 resolution is fixed but haproxy sees it down. Inspect the custom nginx configurations. (Click again "Next Clue/Solution" to reveal the final step).<br><br>
<b>Solution. </b>From <i>custom-nginx_1.conf</i>, nginx_1 is serving from its port :81 (even if <kbd>docker ps -a</kbd> shows it at :80), so you can change <i>custom-nginx_1.conf</i> so that it also uses :80 like nginx_0 or in haproxy.cfg change the last line to <i>nginx_1:81</i>. Restart Docker Compose again and test running <kbd>curl localhost:5000</kbd> a couple times.