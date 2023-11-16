# "Belo-Horizonte": A Java Enigma

## Description

(Credit for the idea: <i>fuero</i>)<br><br>

There is a one-class Java application in your /home/admin directory. Running the program will print out a secret code, or you may be able to extract the secret from the class file without executing it but I'm not providing any special tools for that.<br><br>
Put the secret code in a /home/admin/solution file, eg <kbd>echo "code" >  /home/admin/solution</kbd>.

## Test

<kbd>md5sum /home/admin/solution |awk '{print $1}'</kbd> returns <kbd>9d2bd7aabb26681eacd9444da6b6643c</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(md5sum /home/admin/solution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "9d2bd7aabb26681eacd9444da6b6643c" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```


## Clues

<b>1. </b>Running <kbd>java Sad</kbd> gives a version conflict error. Note that major version 55 is Java 11 and version 61 is Java 17. Run for example <kbd>sudo find / -type f -name java</kbd> to find the different Java installs in this server, or follow from <kbd>which java</kbd> the path to the default java version.<br><br>

<b>2. </b> To fix the Java version issue, relink the <i>java</i> in the path with the java version 17: <kbd>sudo rm /etc/alternatives/java</kbd> ; <kbd>sudo ln -s /usr/lib/jvm/java-17-openjdk-amd64/bin/java /etc/alternatives/java</kbd> or use <i>/usr/lib/jvm/java-17-openjdk-amd64/bin/java</i><br><br>

<b>3. </b> Executing now <kbd>java Sad</kbd> gives an <kbd>java.lang.NoClassDefFoundError: VerySad (wrong name: Sad)</kbd>. From that error or <kbd>javap -verbose Sad.class</kbd> we see we the file name should be changed: <kbd>mv Sad.class VerySad.class</kbd><br><br>

<b>4. </b>If we run now <kbd>java VerySad</kbd> we get <kbd>Exception in thread "main" java.lang.OutOfMemoryError: Java heap spac</kbd>. The default JVM heap is small (50% available RAM up to 512MB). Let's try assigning fixed bigger size: <kbd>java -Xms1g -Xmx1g VerySad</kbd><br><br>

<b>5. </b>We are still running out of memory. We have about 400 MB of available RAM from <kbd>free -m</kbd> for example. And we have about 5 GB of free disk space from <kbd>df -h</kbd>. We can create a swap partition.<br><br>

<b>6. </b>to add a swap file (we can try 1GB or 2GB):<kbd>sudo fallocate -l 1G /swapfile</kbd> ,<kbd> sudo mkswap /swapfile</kbd>, <kbd>sudo chmod 600 /swapfile</kbd> and <kbd>sudo swapon /swapfile</kbd>. We can check with <kbd>sudo swapon --show; free -m</kbd><br><br>

<b>7. </b>Finally we can run <kbd>java -Xms1g -Xmx1g VerySad</kbd> which gives us the secret <kbd>YXADJA</kbd> which after killing the program we save in the solution file to verify: <kbd>echo "YXADJA" > solution</kbd>. 