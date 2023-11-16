# "The Command Line Murders"

## Description

This is the <a href="https://github.com/veltman/clmystery" target="_blank">Command Line Murders</a> with a small twist as in the solution is different<br><br>
Enter the name of the murderer in the file <i>/home/admin/mysolution</i>, for example <kbd>echo "John Smith" > ~/mysolution</kbd>
<br><br>
Hints are at the base of the <i>/home/admin/clmystery</i> directory. Enjoy the investigation! 

## Test

<kbd>md5sum ~/mysolution</kbd> returns <kbd>9bba101c7369f49ca890ea96aa242dd5</kbd><br><br>
(You can always see <i>/home/admin/agent/check.sh</i> to see how the solution is evaluated).


<b>check.sh</b>

```
#!/usr/bin/bash
res=$(md5sum /home/admin/mysolution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "9bba101c7369f49ca890ea96aa242dd5" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1.</b>See the tip files in the <i>/home/admin/clmystery</i> directory.<br><br>
<b>2.</b>From tip: suspect has <kbd>blue Honda, with a license plate that starts with "L337" and ends with "9"</kbd> From <kbd>grep "CLUE" crimescene</kbd> we know suspect is a tall male, from the list of car owners it can be only Joe Germuska or Jeremy Bowers.<br><br>
<b>3. (Solution)</b>Even without the "tall male" clue, the only suspect from the car list that belongs to all the clubs is:<kbd>cat memberships/Rotary_Club memberships/Delta_SkyMiles memberships/Terminal_City_Library memberships/Museum_of_Bash_History |grep -c "Joe Germuska"</kbd>

