# "Manhattan": can't write data into database.

## Description

Your objective is to be able to insert a row in an existing Postgres database. The issue is not specific to Postgres and you don't need to know details about it (although it may help).<br><br>Helpful Postgres information: it's a service that listens to a port (:5432) and writes to disk in a data directory, the location of which is defined in the <i>data_directory</i> parameter of the configuration file <i>/etc/postgresql/14/main/postgresql.conf</i>. In our case Postgres is managed by <i>systemd</i> as a unit with name <i>postgresql</i>.

## Test

(from default admin user) <kbd>sudo -u postgres psql -c "insert into persons(name) values ('jane smith');" -d dt</kbd><br><br>Should return:<kbd>INSERT 0 1</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(sudo -u postgres psql -c "insert into persons(name) values ('jane smith');" -d dt)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "INSERT 0 1" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1.</b> Run the test. Is the Postgres server running? You can check with: <kbd>sudo systemctl status postgresql</kbd> or with the <i>ps</i> command, for example: <kbd>ps auxf|grep postgres</kbd><br><br>
<b>2.</b> Try to start <kbd>sudo systemctl start postgresql</kbd> and check status again.<br><br>
<b>3.</b> Check service errors using <i>journalctl</i> , for example <kbd>journalctl -u postgresql</kbd> or <kbd>journalctl -p err</kbd>.<br><br>
<b>4.</b> Check the system log <i>/var/log/syslog</i> , look out for recent <i>postgres</i> messages.<br><br>
<b>5.</b> Check disk space <kbd>df -h</kbd> <br><br>
<b>6.</b> Check if Postgres can't start due to lack of disk space: <kbd>grep -i 'no space left' /var/log/syslog</kbd><br><br>
<b>7.</b> Check the size of the Postgres data directory (for example: <kbd>du -sh /opt/pgdata/main</kbd>) and compare with the size of the volume <i>/opt/pgdata</i><br><br>
<b>Solution:</b> Delete <i>/opt/pgdata/file*.bk</i> files and try to restart Postgres with <kbd>sudo systemctl start postgresql</kbd> 
