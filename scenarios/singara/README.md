# "Singara": Docker and Kubernetes web app not working

## Description

There's a <i>k3s</i> Kubernetes install you can access with <i>kubectl</i>. The Kubernetes YAML manifests under <kbd>/home/admin</kbd> have been applied. The objective is to access from the host the "webapp" web server deployed and find what message it serves (it's a name of a town or city btw). In order to pass the check, the webapp Docker container should not be run separately outside Kubernetes as a shortcut.

## Test

<kbd>curl localhost:8888</kbd> returns a value from the webapp deployed Kubernetes pod.

<b>check.sh</b>

```
#!/usr/bin/bash
key=$(curl -s localhost:8888)
key=$(echo $key|tr -d '\r')
res=$(echo -n $key|md5sum|awk '{print $1}')
res=$(echo $res|tr -d '\r')
res2=$(sudo docker ps -a|grep 8888)

if [[ "$res" = "c6faeb6a2f39140cccf1f69cc3be84cd" && "$res2" = "" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Review K8s and pod state for our namespace: <kbd>kubectl get all -n web</kbd> , <kbd>kubectl describe pod -n web</kbd><br><br>
<b>2. </b>The status of the webapp-deployment is <i>ImagePullBackOff</i>. The webapp pod description says: <i>Failed to pull image "webapp"</i>. Try and <kbd>docker pull webapp</kbd><br><br>
<b>3. </b>Check <kbd>docker images --digests</kbd><br><br>
<b>4. </b>There is a <i>registry</i> image you can use. (Open window once more to see the main solution)<br><br>
<b>5. </b>Create a registry and push the webapp image to it so a digest is added to the image: <kbd>docker run -d -p 5000:5000  registry:2</kbd> ; <kbd>docker tag webapp localhost:5000/webapp</kbd> ; <kbd>docker push localhost:5000/webapp</kbd>. Change the deployment manifest so that <i>image:</i> is <i>localhost:5000/webapp</i> (or pull image from the repository and use that) and deploy: <kbd>kubectl apply -f deployment.yaml</kbd> (Open window again to see the rest of the solution)<br><br>
<b>6. </b>Fix in <i>deployment.yaml</i> for the container spec, <i>containerPort:</i> should be <i>8888</i> , and redeploy.<br>Tunnel from the webapp pod to the local <i>:8888</i> port and <i>curl</i> to it: <kbd>kubectl port-forward deployments/webapp-deployment 8888 -n web &</kbd> ; <kbd>curl localhost:8888</kbd> (another option to get the message from the webapp is to <i>kubectl exec</i> into the pod and curl locally but this is not verified by the "Check Solution" script).