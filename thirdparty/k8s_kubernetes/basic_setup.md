# For Linux
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube

sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/
```
### Ensure minikube starts with enough memory/cpu

```
# Check status of already existing minikube
vboxmanage showvminfo minikube | grep "Memory size\|Number of CPUs"
minikube stop
minikube config set memory 8192
minikube config set cpus 4
minikube start

# or alternatively
vboxmanage modifyvm "minikube" --cpus 4 --memory 8192
```

```
# First time setup
grep -E --color 'vmx|svm' /proc/cpuinfo
cpus=4
mem=6144
minikube start --vm-driver=virtualbox --cpus $cpus --memory $memory
minikube status
kubectl get node minikube -o jsonpath='{.status.capacity}' && echo

```

## Below settings are env variables
```
# GUI
mylan="192.168.1.1"
k8s_host="192.168.1.10"
mylaptop="192.168.1.10"
api_port=8001
sshUser=root
```

## Ensure IP tables are enabled eg for local LAN
```
sudo iptables -I INPUT -s ${mylan}/24 -p tcp --dport ${api_port} -j ACCEPT
sudo iptables -I INPUT -s ${mylan}/24 -p tcp --dport 8443 -j ACCEPT
sudo iptables-save >/etc/iptables/rules.v4
```

### Check settings of context
```
kubectl config view
```


## Apply GUI package
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.4/aio/deploy/recommended.yaml
# Change If necessary to host which is not blocked. NOT necessary mostly as we are enabling 8443 access for LAN
# kubectl config set-cluster minikube --server=https://<samehost>:8443



### Start with localLan and how the address needs exposing
# kubectl proxy --accept-hosts='^localhost$,^192\.168\.+\..+$' --address="${k8s_host}" &
kubectl proxy &   # This is just enough if you are port fowarding
```

### Ensure you have an admin account in the dashboard

```
### Tokens (will take some time)
https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
kubectl -n kubernetes-dashboard get secret

kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
```

### In your laptop, port forward and access as localhost
```
mylan="192.168.2.1"
k8s_host="192.168.2.73"
api_port=8001
sshUser=root
ssh -L ${api_port}:localhost:${api_port} ${sshUser}@${k8s_host}
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
```

```
# To show all services  running within minikube
minikube service  list
```
