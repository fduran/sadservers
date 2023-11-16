# "Pokhara": SSH and other sshenanigans

## Description

A user <kbd>client</kbd> was added to the server, as well as their SSH public key.<br>
The objective is to be able to SSH locally (there's only one server) as this user <i>client</i> using their ssh keys. This is, if as root you change to this user <kbd>sudo su; su client</kbd>, you should be able to login with ssh: <kbd>ssh localhost</kbd>.<br><br>

## Test

As user <i>admin</i>: <kbd>sudo -u client ssh client@localhost 'pwd'</kbd> returns <kbd>/home/client</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(sudo -u client ssh client@localhost 'pwd')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "/home/client" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Running the test you get a "man-in-the-middle" warning, as suggested you can <kbd>sudo -u client ssh-keygen -f "/home/client/.ssh/known_hosts" -R "localhost"</kbd> (note: if you run the command not as <i>client</i> then you need to change the owner of the file to <i>client</i>. You can also delete the file's contents<kbd>> /home/client/.ssh/known_hosts</kbd>.<br><br>

<b>2. </b>
Running the test again adds the correct host key but returns <kbd>client@localhost: Permission denied (publickey).</kbd>. Review the ssh service configuration under /etc/ssh/.<br><br>

<b>3. </b>There's a <i>DenyUsers client</i> entry in the sshd configuration; as root delete the file <kbd>/etc/ssh/sshd_config.d/sad.conf</kbd> and <kbd>systemctl restart ssh</kbd><br><br>

<b>4. </b>Running the test command results in the message: 
<kbd>WARNING: UNPROTECTED PRIVATE KEY FILE!
Permissions 0644 for '/home/client/.ssh/id_rsa' are too open.</kbd>, so we take out "others" permissions for the private key: <kbd>chmod 600 /home/client/.ssh/id_rsa</kbd>.<br><br>

<b>5. </b>Error is now: <kbd>"Your account has expired; please contact your system administrator."</kbd>.
Look at <kbd>lslogins client</kbd> or <kbd>grep client /etc/shadow</kbd>. The "password" (rather account) expiration is set to "0" ("1970-Jan01"), to set to no expiration run as superuser: <kbd>chage -E-1 client</kbd>.<br><br>

<b>6. </b>Now we get the error:<kbd>exec request failed on channel 0</kbd>.
See in <kbd>/etc/pam.d/sshd</kbd> the configuration used <kbd>/etc/security/limits.conf</kbd>, which includes a line to limit the processes for user <i>client<i> to zero: <kbd>client         hard    nproc           0</kbd>. Comment out or delete that line as root.<br><br>

<b>7. </b>Error is now <kbd>"This account is currently not available."</kbd>. Look again at 
<kbd>lslogins client</kbd> or <kbd>grep client /etc/passwd</kbd>, see the shell field set to "nologin". Change it to for example (as root): <kbd>usermod --shell /bin/bash client</kbd> (to see a list of available shells: <kbd>cat /etc/shells</kbd>). This is the last broken thing!