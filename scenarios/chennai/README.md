# "Chennai": Pull a Rabbit from a Hat

## Description

There is a RabbitMQ (RMQ) cluster defined in a docker-compose.yml file. 
<br><br>
Bring this system up and then run the producer.py script in such a way that is able to send messages to RMQ. In particular you have to send the message "hello-lwc".
<br><br>
- RMQ is a queuing system: messages are put in the queue with a "producer" and they are taken out from the other side by a "consumer". The queue name has to be the same for both.
<br><br>
- To send the message "hello-lwc": <kbd>python3 ~/producer.py hello-lwc</kbd>. Should return <kbd>Message sent to RabbitMQ</kbd>. "IncompatibleProtocolError" means RMQ is not working properly.<br><br>
- To test consuming it: <kbd>python3 ~/consumer.py</kbd>, this will retrieve the next message from the queue and print it. Once everything is working send more than one message so there's at least one in the queue when the validation runs.
<br><br>
- <b>Do not change the consumer.py and producer.py files</b>; if you do the Check My Solution will fail.

## Test

<kbd>python3 ~/consumer.py</kbd> returns <kbd>hello-lwc</kbd>
<br><br>
See /home/admin/agent/check.sh for the exact test.

<b>check.sh</b>

```
#!/bin/bash
res=$(nmap -p 5672 localhost|grep open|awk {'print $3'})
res=$(echo $res|tr -d '\r')

if [[ "$res" != "amqp" ]]
then
  echo -n "NO"
  exit -1
fi

res=$(md5sum /home/admin/consumer.py | awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" != "2216a243695c9d7834bdc299e68d051c" ]]
then
  echo -n "NO"
  exit -1
fi

res=$(md5sum /home/admin/producer.py | awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" != "86c470d5822fea6c31293f42f5e0aa34" ]]
then
  echo -n "NO"
  exit -1
fi

res=$(python3 /home/admin/consumer.py)
res=$(echo $res|tr -d '\r')

if [[ "$res" == "hello-lwc" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Starting the containers: <kbd> cd rabbitmq-cluster-docker-master ; docker compose up -d </kbd> shows an issue on the RMQ container you can inspect with <kbd>docker logs</kbd>, showing an issue with a file /var/log/rabbitmq/*.log that does not exist<br><br>
<b>2. </b>Fix the entrypoint in line 26 of cluster-entrypoint.sh , the purpose of this tail -f command is to run any process so the container doesn't exist, you can use in infinite sleep here of for example <kbd>tail -f /var/log/bootstrap.log</kbd><br><br>
<b>3. </b>Once RMQ cluster works properly, trying to send a message to it <kbd>python3 ~/producer.py hello-lwc</kbd> results in an authentication issue. Inspect the code for consumer.py, producer.py and docker-compose.yml<br><br>
<b>4. </b>The consumer.py has hard-coded values for username, password and queue name while the producer.py takes them from env vars (that you can change) and for the RMQ containers they take the user and password from env vars (otherwise they use default values). Next Clue gives the solution<br><br>
<b>Solution </b><kbd>export RABBITMQ_DEFAULT_USER=username; export RABBITMQ_DEFAULT_PASS=password</kbd> and restart docker compose and send the message with: <kbd>RMQ_USER=username RMQ_PASSWORD=password RMQ_QUEUE=hello python3 ~/producer.py hello-lwc</kbd>. An alternative option is to use rabbitmctl to remove all authentication from RMQ.