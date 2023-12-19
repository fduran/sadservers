# "Bilbao": Basic Kubernetes Problems

## Description

There's a Kubernetes Deployment with an Nginx pod and a Load Balancer declared in the manifest.yml file. The pod is not coming up. Fix it so that you can access the Nginx container through the Load Balancer.<br><br>
There's no "sudo" (root) access.

## Test

Running <kbd>curl 10.43.216.196</kbd> returns the default Nginx Welcome page.<br><br>
See <i>/home/admin/agent/check.sh</i> for the test that "Check My Solution" runs.

<b>check.sh</b>

```
#!/usr/bin/bash
# DO NOT MODIFY THIS FILE ("Check My Solution" will fail)

res=$(kubectl get pods -l app=nginx --no-headers -o json | jq -r '.items[] | "\(.status.containerStatuses[0].state.waiting.reason // .status.phase)"')
res=$(echo $res|tr -d '\r')

if [[ "$res" != "Running" ]]
then
  echo -n "NO"
  exit 1
fi

res=$(curl -s 10.43.216.196:80|grep -c Welcome)
if [[ "$res" -eq 2 ]]
then
  echo -n "OK"
else
  echo "NO"
fi
```

## Clues

<b>1. </b> Look at the manifest: <kbd>cat manifest.yml</kbd>. Check the pod status with <kbd>kubectl get pod</kbd> and <kbd>kubectl describe pod/nginx-deployment-$hash</kbd><br><br>
<b>2. </b> From the <kbd>kubectl describe pod</kbd> command we see a message from Kubernetes scheduler: <i>0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector</i>. Add the missing label to the node:  <kbd>kubectl label nodes node1 disk=ssd</kbd> and delete the pod or delete in the manifest the nodeSelector and <kbd>kubectl apply -f manifest.yml</kbd><br><br>
<b>3. </b> The Nginx pod is still not running. From the <kbd>kubectl describe pod</kbd> command again we see a new message from Kubernetes scheduler: <i>0/1 nodes are available: 1 Insufficient memory</i>. Delete or lower in the manifest the resource.requests.memory value and <kbd>kubectl apply -f manifest.yml</kbd>.<br><br>If there's an error pulling the image: <i>ErrImagePull</i>, then there's a problem with the local Docker registry, you can fix it with <kbd>docker restart docker-registry</kbd>.