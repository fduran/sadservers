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