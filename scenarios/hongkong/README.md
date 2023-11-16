# "Hong-Kong": can't write data into database.

## Description

(Similar to "Manhattan" scenario but harder). Your objective is to be able to insert a row in an existing Postgres database. The issue is not specific to Postgres and you don't need to know details about it (although it may help).<br><br>Postgres information: it's a service that listens to a port (:5432) and writes to disk in a data directory, the location of which is defined in the <i>data_directory</i> parameter of the configuration file <i>/etc/postgresql/14/main/postgresql.conf</i>. In our case Postgres is managed by <i>systemd</i> as a unit with name <i>postgresql</i>.

## Test

(from default admin user) <kbd>sudo -u postgres psql -c "insert into persons(name) values ('jane smith');" -d dt</kbd><br><br>Should return:<kbd>INSERT 0 1</kbd>

## Clues

<b>1.</b> Run the test. Is the Postgres server running? You can check with: <kbd>systemctl status postgresql</kbd> or with the <i>ps</i> command, for example: <kbd>ps auxf|grep postgres</kbd><br><br>
<b>2.</b> Try to start Postgres <kbd>systemctl start postgresql</kbd> and check its status again.<br><br>
<b>3.</b> Check errors using <i>journalctl</i> , for example <kbd>journalctl -u postgresql</kbd> or <kbd>journalctl -p err</kbd>.<br><br>
<b>4.</b> A log message says <i>Timed out waiting for device /dev/xvdb.</i>. The postgres data directory is <i>/opt/pgdata/</i> but there's no data there. Check if there is a disk volume that hasn't been mounted.<br><br>
<b>5.</b> Running <kbd>lsblk -f</kbd> you can see there's an unmounted xfs disk and <kbd>file -s /dev/nvme0n1</kbd> confirms it has data (the exact device name may be different). Try and mount the device on the Postgres data directory.<br><br>
<b>6.</b> Trying <kbd>mount /dev/nvme0n1 /opt/pgdata</kbd> does not work. From <kbd>journalctl|tail</kbd> we see: <i>systemd[1]: opt-pgdata.mount: Unit is bound to inactive unit dev-xvdb.dev</i><br><br>
<b>7.</b> <i>systemd</i> controls mounts and reads <i>/etc/fstab</i> , edit <i>/etc/fstab</i> and change <i>/dev/xvdb</i> into <i>/dev/nvme0n1</i> and <kbd>systemctl daemon-reload</kbd>. Now you can: <kbd>mount /dev/nvme0n1 /opt/pgdata</kbd> and check there are postgres files there. Try restarting Postgres now.<br><br>
<b>8.</b> See <i>journalctl</i> log entry <i>No space left on device</i>. Check disk space: <kbd>df -h</kbd> <br><br>
<b>9.</b> Check the size of the Postgres data directory (for example: <kbd>du -sh /opt/pgdata/main</kbd>) and compare with the size of the volume <i>/opt/pgdata</i><br><br>
<b>Solution:</b> Delete <i>/opt/pgdata/file*.bk</i> files and restart Postgres with <kbd>sudo systemctl start postgresql</kbd> 