## Get credentials and run a command
```
gcloud container clusters get-credentials my-gke-cluster --region europe-west1 --project myproject
kubectl exec keycloak-56754df4b4-cc7tv --namespace keycloak -c keycloak -- ls
```
