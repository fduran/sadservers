# "Santiago": Find the secret combination

## Description

Alice the spy has hidden a secret number combination, find it using these instructions:<br><br>
1) Find the number of <b>lines</b> with occurrences of the string <b>Alice</b> (case sensitive) in the <i>*.txt</i> files in the <i>/home/admin</i> directory<br>
2) There's a file where <b>Alice</b> appears exactly once. In that file, in the line after that "Alice" occurrence there's a number.<br>
Write both numbers consecutively as one (no new line or spaces) to the solution file. For example if the first number from 1) is <i>11</i> and the second <i>22</i>, you can do <kbd>echo -n 11 > /home/admin/solution; echo 22 >> /home/admin/solution</kbd> or echo "1122" > /home/admin/solution.

## Test

Running <kbd>md5sum /home/admin/solution</kbd> returns <kbd>d80e026d18a57b56bddf1d99a8a491f9</kbd>(just a way to verify the solution without giving it away.)

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(md5sum /home/admin/solution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "d80e026d18a57b56bddf1d99a8a491f9" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Use <i>grep</i> recursively or use <i>find</i> and pass the results to <i>grep</i> via <i>xargs</i><br><br>(Open window once more to see the solution to the first part).<br><br>
<b>2. </b>(Solution to 1) <kbd>cd /home/admin/</kbd> and then for example: <kbd>grep -rc Alice *.txt</kbd> or <kbd>find . -type f -name "*.txt" |xargs grep -c 'Alice'</kbd> , adding the results from the three files: <kbd>echo -n 411 > /home/admin/solution</kbd><br><br>(Open window once more to see the solution to the second part).<br><br>
3. (Solution to 2) The file with exactly one Alice occurrence is 1342-0.txt :<kbd>grep Alice -A 1 /home/admin/1342-0.txt</kbd> (or open the file with <kbd>less</kbd> or <kbd>vi</kbd> and enter <kbd>/Alice</kbd>). Appending this result: <kbd>echo 156 >> /home/admin/solution</kbd> (The solution is 411156).
