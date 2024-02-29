# "Lisbon": etcd SSL cert troubles

## Description

There's an <i>etcd</i> server running on https://localhost:2379 , get the value for the key "foo", ie <kbd>etcdctl get foo</kbd> or <kbd>curl https://localhost:2379/v2/keys/foo</kbd>

## Test

<kbd>etcdctl get foo</kbd> returns <kbd>bar</kbd>.

<b>check.sh</b>

```
#!/usr/bin/bash
export GODEBUG=x509ignoreCN=0
export ETCDCTL_ENDPOINT=https://localhost:2379
res=$(etcdctl get foo)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "bar" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>Running <kbd>etcdctl get foo</kbd> shows an error: <kbd>certificate has expired or is not yet valid: current time ... is after ...</kbd>, it's clear the server time is one year ahead, to fix set the server time to the actual time, for ex: <kbd>sudo date -s "2023-01-01"</kbd> (Next "clue" gives the solution).<br><br>

<b>2. </b>Not easy to see unless looking for it (for example using <i>tcpdump</i>) but there's an iptables rule that redirects TCP traffic going to the etcd port :2379 into port :443 , and there's an Nginx server listening to that port: <kbd>sudo /usr/sbin/iptables -t nat -L</kbd>, deleting this rule will fix the remaining issue, for ex: <kbd>sudo /usr/sbin/iptables -t nat -F</kbd>