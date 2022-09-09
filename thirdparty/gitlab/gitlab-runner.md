
### To register runner
```
gitlab-runner register --non-interactive --tls-ca-file /etc/my-cert-file.pem --url https://gitlab-server:444 --registration-token SOME2KXB5mH1f35d5 --executor shell --tag-list my-server --config /etc/gitlab-runner/config.toml
```



### Fix registration issue with gitlab runner in k8s 
https://stackoverflow.com/a/58207518
```
## Delete token
k8s_secret="gitlab-gitlab-runner-secret"
kubectl -n gitlab delete secret generic $k8s_secret


## Now have to clear from PostGres DB
# The task runner pod will have the gitlab-rake rails tools
pod="gitlab-task-runner-7d65759bc6-jp5s8"
kubectl -n gitlab exec -it $pod  -- /bin/bash


gitlab-rails dbconsole
-- Clear project tokens
UPDATE projects SET runners_token = null, runners_token_encrypted = null;
-- Clear group tokens
UPDATE namespaces SET runners_token = null, runners_token_encrypted = null;
-- Clear instance tokens
UPDATE application_settings SET runners_registration_token_encrypted = null;
-- Clear key used for JWT authentication
-- This may break the $CI_JWT_TOKEN job variable:
-- https://gitlab.com/gitlab-org/gitlab/-/issues/325965
UPDATE application_settings SET encrypted_ci_jwt_signing_key = null;
-- Clear runner tokens
UPDATE ci_runners SET token = null, token_encrypted = null;


## Register token again
reg_token="xyzVt16P234mynRT"
kubectl -n gitlab create secret generic $k8s_secret --from-literal=runner-registration-token=$reg_token --from-literal=runner-token=""

```

### Reset root password
```
pod="gitlab-task-runner-7d65759bc6-jp5s8"
kubectl -n gitlab exec -it $pod  -- /bin/bash

gitlab-rake "gitlab:password:reset[root]"

```

### Gitlab runner k8s config
- Ensure k8s secret is created with `my-cert`
```
image: myrepo/group1/gitlab-runner:centos8
imagePullPolicy: IfNotPresent
gitlabUrl: "https://myserver:5443"
certsSecretName: my-cert

runners:
  # runner configuration, where the multi line strings is evaluated as
  # template so you can specify helm values inside of it.
  #
  # tpl: https://helm.sh/docs/howto/charts_tips_and_tricks/#using-the-tpl-function
  # runner configuration: https://docs.gitlab.com/runner/configuration/advanced-configuration.html
  config: |
    [[runners]]
      [runners.kubernetes]
        namespace = "{{.Release.Namespace}}"
        image = "myrepo/group1/my-image:v1"
        helper_image = "myrepo/group2/gitlab-runner-helper:alpine3.15-x86_64-a2003406"
        tls-ca-file = "/home/gitlab-runner/.gitlab-runner/certs/my-cert.crt"
```
