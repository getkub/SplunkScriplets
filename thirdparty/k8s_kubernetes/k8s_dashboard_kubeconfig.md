## Steps to Generate kubeconfig


### Vars which are setup as part of the dashboard
```
export K8S_DB_USER=admin-user
#export K8S_DB_USER=kubernetes-dashboard
export K8S_NS=kubernetes-dashboard
```

### Export Variables
```
export USER_TOKEN_NAME=$(kubectl -n ${K8S_NS} get serviceaccount ${K8S_DB_USER} -o=jsonpath='{.secrets[0].name}')
export USER_TOKEN_VALUE=$(kubectl -n ${K8S_NS} get secret/${USER_TOKEN_NAME} -o=go-template='{{.data.token}}' | base64 --decode)
export CURRENT_CONTEXT=$(kubectl config current-context)
export CURRENT_CLUSTER=$(kubectl config view --raw -o=go-template='{{range .contexts}}{{if eq .name "'''${CURRENT_CONTEXT}'''"}}{{ index .context "cluster" }}{{end}}{{end}}')
export CLUSTER_CA=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}')
export CLUSTER_SERVER=$(kubectl config view --raw -o=go-template='{{range .clusters}}{{if eq .name "'''${CURRENT_CLUSTER}'''"}}{{ .cluster.server }}{{end}}{{ end }}')
```

### Now generate the kubeconfig file
```
# Changing to a temp directory would be good
cd /tmp/
```

```
cat << EOF > k8s_dashboard
apiVersion: v1
kind: Config
users:
 - name: ${K8S_NS}
   user: 
     token: ${USER_TOKEN_VALUE}
clusters:
- cluster:
    certificate-authority-data: ${CLUSTER_CA}
    server: ${CLUSTER_SERVER}
  name: ${CURRENT_CONTEXT}
contexts:
- context:
    cluster: ${CURRENT_CONTEXT}
    user: ${K8S_NS}
    namespace: ${K8S_NS}
  name: ${CURRENT_CONTEXT}
current-context: ${CURRENT_CONTEXT}
EOF
```


### Test the kubeconfig file
```
kubectl --kubeconfig $(pwd)/k8s_dashboard get all --all-namespaces
```
