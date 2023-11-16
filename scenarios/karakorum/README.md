# "Karakorum": WTFIT – What The Fun Is This?

## Description

There's a binary at <kbd>/home/admin/wtfit</kbd> that nobody knows how it works or what it does (<i>"what the fun is this"</i>). Someone remembers something about <i>wtfit</i> needing to communicate to a service in order to start. Run this <i>wtfit</i> program so it doesn't exit with an error, fixing or working around things that you need but are broken in this server. (Note that you can open more than one web "terminal").

## Test

<kbd>/home/admin/wtfit</kbd> returns <kbd>OK.</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(cd /home/admin && ./wtfit)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "OK." ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>chmod is not executable. This is a fun (granted, unrealistic) problem that is popular for the different inventive ways to fix it, so a web search to find solutions is easy :-)<br><br>
<b>2. </b>(solution to chmod issue) To make chmod executable you can write some code like: <kbd>sudo perl -e 'chmod 0755, "/usr/bin/chmod"'</kbd> or <kbd>/lib64/ld-linux-x86-64.so.2 /usr/bin/chmod +x /usr/bin/chmod</kbd>, then you can do <kbd>chmod +x /home/admin/wtfit</kbd><br><br>
<b>3. </b>Upon execution of wtfit you get <kbd>ERROR: can't open config file</kbd>. You need to introspect the code or the system calls to find out the name and location that the program is expecting and create that file.<br><br>
<b>4. </b>(Solution to config file) do <kbd>strace /home/admin/wtfit</kbd> and towards the end see the entry <kbd>openat(AT_FDCWD, "/home/admin/wtfitconfig.conf", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)</kbd> , create the missing file, for ex: <kbd>touch /home/admin/wtfitconfig.conf</kbd><br><br>
<b>5. </b>Now wtfit gives an <kbd>ERROR: can't connect to server</kbd>. You need to look in the network for where the program is trying to communicate to, and create a network service that can listen to the network request.<br><br>
<b>6. </b>Run tcpdump to sniff the network and while running, execute wtfit: <kbd>sudo tcpdump -i lo &</kbd> only listen to <i>localhost</i>, or all ports except our "ssh": <kbd>sudo tcpdump -i any port not 8080 &</kbd><br><br>
<b>7. </b>Filtering other traffic, you'll see this packet <kbd>IP localhost.40302 > localhost.7777: Flags [S], seq 1326851547, win 65495, options ...</kbd> (initiator port will vary )<br><br>
<b>8. </b>(Solution to last issue) Run a server on <i>tcp:7777</i>, for ex: <kbd>python3 -m http.server 7777 &</kbd> (there's also nginx, apache and netcat installed or you could redirect with iptables to an existing service).
