# "Monaco": Disappearing Trick

## Description

There is a web server on :5000 with a form. POSTing the correct form password into this web service will return a secret.
<br><br>
Save this secret provided by the web page (not the password you sent to it)  to /home/admin/mysolution, for example: <kbd>echo "SecretFromWebSite" > ~/mysolution</kbd>
<br><br>
TIP: a developer worked on the web server code in this VM, using the same 'admin' account.
<br><br>
Scenario credit: PuppiestDoggo

## Test

<kbd>md5sum /home/admin/mysolution</kbd> returns <kbd>a250aa19f16dda6f9fcef286f035ec4b</kbd>

<b>check.sh</b>

```
#!/bin/bash

expected_checksum="a250aa19f16dda6f9fcef286f035ec4b"
actual_checksum=$(md5sum /home/admin/mysolution | awk '{print $1}')

if [[ "$actual_checksum" == "$expected_checksum" ]]; then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Check the web server form: <kbd>curl localhost:5000</kbd>, you can try posting a random password: <kbd>curl -d "password=12345" -X POST localhost:5000</kbd> that will return <kbd>Access denied!</kbd><br><br>
<b>2. </b>From the tip that a developer worked with this 'admin' account, you can check <kbd>ls -lah</kbd> to find a <kbd>.git</kbd> directory. Try and see what's in there.<br><br>
<b>3. </b>Doing <kbd>git status</kbd> or <kbd>git diff</kbd> for example will show you a deleted file you can recover with:<kbd>git restore webserver_v1.py</kbd> <br><br>
<b>4. </b>Inspecting the file we see the code accepts the password submitted if it's equal than the environment variable SUPERSECRETPASSWORD<br><br>
<b>5. </b>This env var is not in your current environment (<kbd>env</kbd>) but used by the application, which runs on your same "admin" user account as you can inspect with "ps". The file "webserver.py" running is present only in memory, not on disk. So what's left is to find the env vars of this process.<br><br>
<b>6. </b>Find the env var SUPERSECRETPASSWORD from "/proc": <kbd>cat /proc/$PID/environ</kbd> , note that the file is a binary so "grep" fails but it's very readable. You can replace the null separating character using "tr", for example: <kbd>| tr "\0" " "</kbd><br><br>
<b>7. </b>POST the SUPERSECRETPASSWORD to the web server to get the requested secret: <kbd>curl -d "password=XIo14t0NYm7W" -X POST localhost:5000</kbd> (Note this password you are posting is generated randomly and changes in every run), the web server should return QhyjuI98BBvf : <kbd>echo "QhyjuI98BBvf" > ~/mysolution</kbd><br><br>
