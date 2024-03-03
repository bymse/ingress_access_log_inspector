# Setup nginx-ingress

Edit `ingress-nginx-controller` ConfigMap to add the following lines:

```yaml
data:
  log-format-escape-json: "true"
  log-format-upstream: '{ "time_local": "$time_iso8601", "remote_addr": "$remote_addr", "request_id": "$request_id",
    "host": "$host", "request_method": "$request_method", "request_uri": "$request_uri", 
    "status": "$status", "http_referer": "$http_referer", "http_user_agent": "$http_user_agent"
    }'
```

Restart the `ingress-nginx-controller` pod to apply the changes.

```bash
kubectl rollout restart -n ingress-nginx deployment/ingress-nginx-controller
```