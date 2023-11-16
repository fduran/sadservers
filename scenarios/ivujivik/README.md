# "Ivujivik": Parlez-vous Français?

## Description

Given the CSV file <i>/home/admin/table_tableau11.csv</i>, find the <i>Electoral District Name/Nom de circonscription</i> that has the largest number of <i>Rejected Ballots/Bulletins rejetés</i> and also has a population of less than 100,000.
<br><br>
The initial CSV file may be corrupted or invalid in a way that can be fixed without changing its data.
<br><br>
Installed in the VM are: Python3, Go, sqlite3, <a href="https://miller.readthedocs.io/en/latest/" target="_blank">miller</a> directly and PostgreSQL, MySQL in Docker images.
<br><br>
Save the solution in the /home/admin/mysolution , with the name as it is in the file, for example: <kbd>echo "Trois-Rivières" > ~/mysolution</kbd>

## Test

<kbd>md5sum</kbd> /home/admin/mysolution returns <kbd>e399d171f21839a65f8f8ab55ed1e1a1</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(md5sum /home/admin/mysolution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "e399d171f21839a65f8f8ab55ed1e1a1" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi

```

## Clues

<b>1. </b>There are many ways of solving this, like writing a bit of Python code for example or using awk. Here I'll show how to solve it using sqlite3 (Mysql and Postgres will have similar solutions). Get a prompt with <kbd>sqlite3</kbd> and import the file as a table: <kbd>.import --csv /home/admin/table_tableau11.csv elect</kbd><br><br>
<b>2. </b>That import give an issue in line 101: exit sqlite3 and fix the missing comma: <kbd>nano +101 table_tableau11.csv</kbd> and try importing again<br><br>
<b>3. </b>We have a table with the data but the numbers are represented as text. We can look at the schema with <kbd>.schema elect</kbd> and see what we can recreate the table by copying the schema output and changing "Population" and "Rejected Ballots/Bulletins rejetés" from TEXT to INTEGER. Now we can <kbd>.import</kbd> again to the new empty table (Next Clue reveals the solution<br><br>
<b>Solution </b>Now we can run the query: <kbd>select "Electoral District Name/Nom de circonscription" from elections where "Population" < 100000 order by "Rejected Ballots/Bulletins rejetés" desc limit 1;</kbd> which returns <kbd>Montcalm</kbd><br><br>
