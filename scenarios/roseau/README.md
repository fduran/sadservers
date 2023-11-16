# "Roseau": Hack a Web Server

## Description

There is a secret stored in a file that the local Apache web server can provide. Find this secret and have it as a /home/admin/secret.txt file.<br><br>
Note that in this server the <i>admin</i> user is not a sudoer.<br><br>
Also note that the password crackers <i>Hashcat</i> and <i>Hydra</i> are installed from packages and <i>John the Ripper</i> binaries have been built from source in <i>/home/admin/john/run</i> 

## Test

<kbd>sha1sum /home/admin/secret.txt |awk '{print $1}'</kbd> returns <kbd>cc2c322fbcac56923048d083b465901aac0fe8f8</kbd>


<b>check.sh</b>

```
#!/usr/bin/bash
res=$(sha1sum /home/admin/secret.txt |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "cc2c322fbcac56923048d083b465901aac0fe8f8" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>We can see one file <i>webfile</i> with <kbd>ls -l /var/www/html/</kbd> and we don't have direct access to it, let's try and check web access with <kbd>curl localhost</kbd><br><br>
<b>2. </b>Apache is asking for credentials, we can see with <kbd>/etc/apache2/sites-enabled/000-default.conf</kbd> that it has basic authentication enanbled. We cannot edit this config file but we can try and break the <kbd>/etc/apache2/.htpasswd</kbd> file.<br><br>
<b>3. </b>Running John the Ripper <kbd>cd ~ ; john/run/john /etc/apache2/.htpasswd</kbd> we obtain the Apache password of the user <i>carlos</i>, run curl again passing user:password<br><br>
<b>4. </b>Running <kbd>curl localhost -u "carlos:chalet"</kbd> we see <i>webfile</i>, we can grab it and save it as <i>secret</i>: <kbd>curl localhost/webfile -u "carlos:chalet" --output secret</kbd><br><br>
<b>5. </b>We check with <kbd>file secret</kbd> that the file is a Zip archive. If we try to <kbd>unzip secret</kbd> we see it is password-protected.<br><br>
<b>6. </b>You can use <i>zip2john</i> to extract the hash and then use <i>john</i> again to find the password for the zip file: <kbd>john/run/zip2john secret > zip.hash</kbd> then <kbd>john/run/john zip.hash</kbd>.<br><br>
<b>7. </b>The previous step yield the password <i>andes</i> for the zip file of the secret, we can now just <kbd>unzip secret</kbd>, which creates a secret.txt file with the secret as asked.
