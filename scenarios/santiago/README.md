# "Santiago": Find the secret combination

## Description

Bob finds himself enamored with Alice, who is more interested in solving problems on the sadservers.com than going on a date. Recognizing that Alice enjoys a good challenge, Bob decides to win her over by impressing her with his problem-solving skills.

Alice, aware of Bob's weak grasp of Linux, crafts a unique challenge for him. She challenges Bob to uncover a secret number hidden in text files, cleverly incorporating her name into some of them. 

The challenge involves:

1. Counting the number of lines in all the *.txt files where Alice has discreetly inscribed her name <b>"Alice"</b>, considering case sensitivity. This count becomes the first part of the secret number, denoted as x. (x can have any number of digits).
2. Identifying a special text file where the word <b>"Alice"</b> appears <b>just once</b>. The second part of the secret number, named y, is the numerical value that <b>immediately follows the string "Alice"</b> in this unique file. (y can also have any number of digits)


To successfully win Alice's attention, Bob must <b>concatenate x and y</b> and write the result in the solution file. 

For example, if <i> x = 11 </i> and <i> y = 22 </i>, Bob should write <i>1122</i> in the solution file located at <i> /home/admin/solution </i>.

<kbd>echo -n 11 > /home/admin/solution; echo 22 >> /home/admin/solution</kbd>

or

<kbd>echo "1122" > /home/admin/solution</kbd>

Bob, recognizing his weakness in Linux, seeks your assistance in solving this challenge. By helping Bob succeed, you not only assist your dear friend but also pave the way for a potential romantic connection with Alice. Can you lend a hand in this Linux adventure?

<b> Note: For the scope of this problem, you only need to check all the *.txt files in /home/admin directory for numbers x and y. </b>


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
