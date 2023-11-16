# "Salta": Docker container won't start.

## Description

There's a "dockerized" Node.js web application in the <kbd>/home/admin/app</kbd> directory. Create a Docker container so you get a web app on port <i>:8888</i> and can <i>curl</i> to it. For the solution to be valid, there should be only one running Docker container.

## Test

<kbd>curl localhost:8888</kbd> returns <kbd>Hello World!</kbd> from a running container.

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(curl -s localhost:8888)
res2=$(sudo docker ps --format "{{.Ports}}" |grep -c '8888->8888/tcp')
res2=$(echo $res2|tr -d '\r')

if [[ "$res" = "Hello World!" && "$res2" = "1" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>(You need to be superuser to run Docker; use <kbd>sudo</kbd> for the commands). Check current images and containers with <kbd>docker images; docker ps -a</kbd><br><br>
<b>2. </b>Check logs with <kbd>docker logs container_name</kbd><br><br>
<b>3. </b>You can try and <kbd>docker run</kbd> using a different entrypoint or command if there's an issue with the executable. (Open window once more to see a partial solution).<br><br>
<b>4. </b>In Dockerfile, in the <i>CMD</i> line change <i>serve.js</i> to <i>server.js</i> and rebuild the image (from the <i>/home/admin/app</i> directory and using an image name like "app" here for ex): <kbd>docker build -t app .</kbd> (use the local <i>node:15.7-alpine</i> provided image, there's no Internet access to pull other ones).<br>You could run as well <kbd>docker run -d app node server.js</kbd> to fix this issue.<br><br>
<b>5. </b>Check the exposed port we want in the container.<br><br>
<b>6. </b>Stop the nginx server running on the same port and restart the container.(Open window once more to see the solution).<br><br>
<b>7. </b>In the Dockerfile, in the <i>EXPOSE</i> line change port <i>8880</i> to <i>8888</i> and rebuild the image. Run with: <kbd>docker run -d -p 8888:8888  app</kbd> (where <i>app</i> is your Docker image name). Or without fixing and rebuilding the image you could <kbd>docker run -d -p 8888:8888 app</kbd> or <kbd>docker run -d -p 8888:8888 app node server.js</kbd>.