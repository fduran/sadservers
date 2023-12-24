# "Marrakech": Word Histogram

## Description

Find in the file <i>frankestein.txt</i> the <strong>second</strong> most frequent word and save in <strong>UPPER</strong> (capital) case in the <i>/home/admin/mysolution</i> file.
<br><br>
A word is a string of characters separated by space or newlines or punctuation symbols <kbd>.,:;</kbd> . Disregard case ('The', 'the' and 'THE' is the same word) and for simplification consider the apostrophe as another character not as punctuation ("it's" would be a word, distinct from "it" and "is"). Also disregard plurals ("car" and "cars" are different words) and other word variations (don't do "stemming").
<br><br>
We are providing a shorter <i>test.txt</i> file where the second most common word in upper case is "WORLD", so we could save this solution as: <kbd>echo "WORLD" > /home/admin/mysolution</kbd>
<br><br>This problem can be done with a programming language (Python, Golang and sqlite3) or with common Linux utilities.

## Test

<kbd>echo "SOLUTION" | md5sum</kbd> returns <kbd>19bf32b8725ec794d434280902d78e18</kbd>
<br><br>
See <i>/home/admin/agent/check.sh</i> for the test that "Check My Solution" runs.

check.sh

```
#!/usr/bin/bash
# DO NOT MODIFY THIS FILE ("Check My Solution" will fail)

res=$(md5sum /home/admin/mysolution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "19bf32b8725ec794d434280902d78e18" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b> You can use the translation utility <a href="https://linuxcommand.org/lc3_man_pages/tr1.html" target="_blank">tr</a> to take out spaces and newlines with repetition (with test file): <kbd>cat test.txt|tr -s ' ' '\n'</kbd><br><br>
<b>2. </b> Next you can delete the punctuation symbols, piping to the previous result: <kbd>| tr -d '.,:;'</kbd><br><br>
<b>3. </b> Then we can transform the resulting words all into upper case by adding: <kbd>tr '[:lower:]' '[:upper:]'</kbd> (Next "Clue" reveals the full solution)<br><br>
<b>4. </b> Finally we can group (sort) the words, count by frequency (uniq) and sort the result (reversed; biggest number first) with <kbd>sort|uniq -c|sort -r</kbd>. To get the first 10 most frequent words we can add for example <kbd>|head -10</kbd>. Complete command: <kbd>cat frankestein.txt|tr -s ' ' '\n'| tr -d '.,:;'|tr '[:lower:]' '[:upper:]'|sort|uniq -c|sort -r |head -10</kbd> So the solution is "AND".

