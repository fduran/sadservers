# "Kihei": Surely Not Another Disk Space Scenario

## Description

There is a <i>/home/admin/kihei</i> program. Make the changes necessary so it runs succesfully, without deleting the <i>/home/admin/datafile</i> file.

## Test

Running <kbd>/home/admin/kihei</kbd> returns <kbd>Done.</kbd>.

<b>check.sh</b>

```
#!/usr/bin/bash
# 6GB datafile exists
res=$(ls -l /home/admin/datafile |cut -d' ' -f 5)
res=$(echo $res|tr -d '\r')

if [[ "$res" != "5368709120" ]]
then
  echo -n "NO"
  exit
fi

# kihei binary didn't change
res=$(md5sum /home/admin/kihei |cut -d' ' -f 1)
res=$(echo $res|tr -d '\r')

if [[ "$res" != "79387f23f56e732aa789ee22761f8b84" ]]
then
  echo -n "NO"
  exit
fi

# kihei runs succesfully
res=$(/home/admin/kihei)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "Done." ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Running <kbd>strace ./kihei</kbd> or <kbd>./kihei -v</kbd> (from <kbd>./kihei -h</kbd> and other combinations), we see that the program tries to create a 1.5GB (1500000000 bytes) file <i>/home/admin/data/newdatafile</i> and there's not enough disk space.<br><br>
<b>2. </b>From <kbd>lsblk -l</kbd> we see two available disks: <i>/dev/nvme1n1</i> and <i>/dev/nvme2n1</i> of 1GB each. We need to create a logical volume that spans both disks.<br><br>
<b>3. </b>To create LV, as superuser: <kbd>pvcreate /dev/nvme1n1 /dev/nvme2n1</kbd>, <kbd>vgcreate vg /dev/nvme1n1 /dev/nvme2n1</kbd>, <kbd>lvcreate -n lv -l 100%FREE vg</kbd>, <kbd>mkfs.ext4 /dev/vg/lv</kbd><br><br>
<b>4. </b>Mount the LV on the data dir and change ownership back to admin user: <kbd>mount /dev/vg/lv /home/admin/data</kbd> , <kbd>chown -R admin: /home/admin/data</kbd><br><br>
<b>5. </b>Run <kbd>~/kihei</kbd> as admin (program can be run many times since it deletes the <i>newdatafile</i> if it exists before re-creating it)