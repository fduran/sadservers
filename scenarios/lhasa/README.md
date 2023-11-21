# "Lhasa": Easy Math

## Description

There's a file <i>/home/admin/scores.txt</i> with two columns (imagine the first number is a counter and the second one is a test score for example).<br><br>
Find the average (more precisely; the arithmetic mean: sum of numbers divided by how many numbers are there) of the numbers in the second column (find the average score).<br><br>
Use exaclty two digits to the right of the decimal point. i. e., <b>use exaclty two "decimal digits" without any rounding</b>. Eg: if average = 21.349 , the solution is 21.34. If average = 33.1 , the solution is 33.10.<br><br>
Save the solution in the <i>/home/admin/solution</i> file, for example: <kbd>echo "123.45" > ~/solution</kbd> 
<br><br>
Tip: There's bc, Python3, Golang and sqlite3 installed in this VM.

## Test

<kbd>md5sum /home/admin/solution</kbd> returns <kbd>6d4832eb963012f6d8a71a60fac77168  solution</kbd>

<b>check.sh</b>

```
#!/usr/bin/bash
# DO NOT MODIFY THIS FILE ("Check My Solution" will fail)
res=$(md5sum /home/admin/solution |awk '{print $1}')
res=$(echo $res|tr -d '\r')

if [[ "$res" = "6d4832eb963012f6d8a71a60fac77168" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>There are many ways of solving this, like writing code or loading the data in a database. A simple way is to use the "bc" command-line calculator to compute the sum of the numbers ("scores") in the second column. Those scores can be easily extracted with <i>awk</i> or <i>cut</i>: <kbd>awk '{ print $2 }' scores.txt</kbd><br><br>
<b>2. </b>We can use the <i>paste</i> tool to add a plus simbol between the score numbers, so we can pass the expression to <i>bc</i>: <kbd>sumexpr=$(awk '{ print $2 }' scores.txt | paste -sd+)</kbd><br><br>
<b>3. </b>The sum of the numbers in the second column would be then: <kbd>sum=$(echo $sumexpr | bc)</kbd> , this returns <i>520.4</i> (regardless of bc "scale" or number of digits to the right of the decimal point). (Click Next to reveal the final solution<br><br>
<b>4. </b>Finally we need to divide the sum of numbers by the amount of them, resulting at the end in two digital numbers. As number of elements (rows) we have elements=100 of them (using <kbd>elements=$(wc -l scores.txt|awk '{ print $1 }')</kbd> for example, being careful with having a new line at the last line). Dividing with a bc "scale" of two and writing to the solution file: <kbd>echo "scale=2; $sum/$elements"|bc > ~/solution</kbd> (Answer is 5.20).  

Alternative solution using a database and SQL:

```
#!/bin/bash

# File with the generated values
input_file="scores.txt"

# SQLite database file
database_file="scores.db"

# Create an SQLite table
sqlite3 "$database_file" <<EOF
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    counter INTEGER,
    score REAL
);
EOF

# Read the input file and insert values into the SQLite table
while read -r line; do
    counter=$(echo "$line" | awk '{print $1}')
    score=$(echo "$line" | awk '{print $2}')
    
    sqlite3 "$database_file" <<EOF
    INSERT INTO scores (counter, score) VALUES ($counter, $score);
EOF
done < "$input_file"

# Compute the average
average=$(sqlite3 -csv "$database_file" "SELECT CAST(AVG(score) AS DECIMAL(10,2)) FROM scores;")
echo "Average Score: $average"
```
