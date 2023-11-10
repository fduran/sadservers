# "Saint John": what is writing to this log file?

## Description

A developer created a testing program that is continuously writing to a log file <i>/var/log/bad.log</i> and filling up disk. You can check for example with <kbd>tail -f /var/log/bad.log</kbd>.<br>
This program is no longer needed. Find it and terminate it.

## Test

The log file size doesn't change (within a time interval bigger than the rate of change of the log file).<br><br>
The "Check My Solution" button runs the script <i>/home/admin/agent/check.sh</i>, which you can see and execute.

check.sh
```
#!/usr/bin/bash

log_file="/var/log/bad.log"

if [ -f "$log_file" ]; then
    current_size=$(stat -c %s "$log_file")
    sleep 0.5
    new_size=$(stat -c %s "$log_file")

    if [ "$current_size" -eq "$new_size" ]; then
        echo -n "OK"
    else
        echo -n "NO"
    fi
else
    echo -n "NO"
fi
```

## Clues

<b>1.</b> You can use <i>ps</i> to list all processes and see if you see something related, for example with: <kbd>ps auxf</kbd>. Ignore system processes [in brackets].<br><br>
A better way is to use the command to list open files: <kbd>lsof</kbd>.<br><br>

<b>2.</b> Find the name (first column) and Process ID (PID, second column) of the process related to <i>/var/log/bad.log</i> by running <i>lsof</i> and filtering the rows to the one(s) containing <i>bad.log</i>.<br><br>You can also use the "fuser" command to quickly find the offending process: <kbd>fuser /var/log/bad.log</kbd>.<br><br>

<b>3.</b> Run: <kbd>lsof |grep bad.log</kbd> and get the PID (second column).<br><br> With the PID of the process, it's not necessary but we can find its current working directory (program location) by doing <kbd>pwdx PID</kbd> or for more detail: <kbd>lsof -p PID</kbd> and check the <i>cwd</i> row. This will allow us to check its ownership and perhaps inspect its offending code if it's a script (not a binary).<br><br>(Open window once more to see the complete solution).<br><br>

<b>4. Solution:</b> Using the PID found, terminate (kill) the process with <kbd>kill -9 PID</kbd>.
