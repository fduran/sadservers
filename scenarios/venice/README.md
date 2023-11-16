# "Venice": Am I in a container?

## Description

Try and figure out if you are inside a container (like a Docker one for example) or inside a Virtual Machine (like in the other scenarios).

## Test

This scenario doesn't have a test (hence also no "Check My Solution" either).

## Clues

<b>1. </b>There are no clues, contact me if you can think of any that won't immediately give away the solution. (Open window once more to see the solution).<br><br>
<b>Solution: </b>This is in fact a Podman container :-) <br>You can get the image: <i>docker.io/fduran/venice</i>.
<br><br>A way of checking is by looking at the environment of the PID=1 process and see if there's a container variable, for ex: <kbd>cat /proc/1/environ|tr "\0" "\n"|grep container</kbd> , in our case would be <i>container=podman</i> but I changed its value.<br><br>An indicator is to look at the running processes and see that there are no kernel threads like <i>[kthreadd]</i>.