# "Buenos Aires": Kubernetes Pod Crashing

## Description

There are two pods: "logger" and "logshipper" living in the default namespace. Unfortunately, logshipper has an issue (crashlooping) and is forbidden to see what logger is trying to say. Could you help fix Logshipper?
<br><br>
Do not change the K8S definition of the logshipper pod. Use "sudo".
<br><br>Because k8s takes a minute or two to change the pod state initially, the check for the scenario is made to fail in the first two minutes.
<br><br>Credit <a href="https://www.linkedin.com/in/srivatsav-kondragunta/">Srivatsav Kondragunta</a>

## Test

<kbd>kubectl get pods -l app=logshipper --no-headers -o json | jq -r '.items[] | "\(.status.containerStatuses[0].ready)"'</kbd>  returns <kbd>true</kbd>


<b>check.sh</b>

```
#!/usr/bin/bash
# DO NOT MODIFY THIS FILE ("Check My Solution" will fail)

res=$(uptime | cut -d' ' -f4)
if [[ "$res" == "0" || "$res" == "1" || "$res" == "2" ]]
then
  echo -n "NO"
  exit
fi

res=$(sudo kubectl get pods -l app=logshipper --no-headers -o json | jq -r '.items[] | "\(.status.containerStatuses[0].ready)"')
res=$(echo $res|tr -d '\r')

if [[ "$res" != "true" ]]
then
  echo -n "NO"
  exit
fi


res=$(sudo k3s kubectl get pods -l app=logshipper --no-headers -o custom-columns=":.spec.serviceAccountName")
res=$(echo $res|tr -d '\r')

if [[ "$res" = "logshipper-sa" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1.</b> (As sudo) View the logs of the logshipper pod to see why it is failing: <kbd>kubectl get pod --show-labels</kbd> and <kbd>kubectl describe pod -l app=logshipper</kbd>.<br><br> 

<b>2.</b> You can view the logshipper pod configuration with the previous "describe" command to see the service account attached to the pod. Once you find that, look for the cluster role binding to see which cluster role the service account is attached to with <kbd>kubectl get ClusterRole</kbd><br><br>

<b>3.</b> Using the cluster role found <i>logshipper-cluster-role</i>, edit it to include the <i>get</i> and <i>watch</i> verbs in the cluster roles (this will default to Vim editor, to emulate the Esc key you can use <kbd>Ctrl [</kbd> ) <kbd>kubectl edit ClusterRole logshipper-cluster-role</kbd><br><br>

<b>4.</b>You may need to restart the logshipper pod. In a Deployment we can just <i>kubectl delete pod logshipper-</i>. We can also: <kbd>kubectl rollout restart deployment logshipper</kbd> or we can <kbd>kubectl scale deployment</kbd> down (--replicas=0) and up (--replicas=1) again.
