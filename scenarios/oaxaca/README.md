# "Oaxaca": Close an Open File

## Description

The file <i>/home/admin/somefile</i> is open for writing by some process. Close this file without killing the process.

## Test

<kbd>lsof /home/admin/somefile</kbd> returns nothing.

check.sh
```
#!/usr/bin/bash
res=$(lsof /home/admin/somefile)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```


## Clues

<b>1. </b>Find the File Descriptor number (FD) with: <kbd>lsof /home/admin/somefile</kbd><br><br>

<b>2. </b>Use the "exec" built-in Bash command with the FD found <i>(77)</i> <a href="https://man7.org/linux/man-pages/man1/exec.1p.html" target="_blank">exec man page</a> (Next "clue" gives the solution).<br><br>

<b>Solution: </b>The file <i>somefile</i> was open by the shell as per <i>lsof</i> (run for example <kbd>ls -la /proc/$$/fd/</kbd>, where <i>$$</i> returns the PID of the current shell). To close the FD: <kbd>exec 77>&-<kbd>