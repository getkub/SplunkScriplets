## Trigger a cross repository CI/CD pipeline

- In your config Repo
```
trigger_automate:
  stage: build
  trigger:
    project: team/repo
    branch: main
    strategy: depend
  rules:
    - changes:
        - triggers/rules_trigger.csv
```

- Once that file is change, this will trigger into the automation repo
- Automation repo

```
trigger_from_config:
  tags:
    - myprod
  stage: build
  image: 
    name: $RUNNER_IMAGE
  script:
    - export ANSIBLE_CONFIG=ansible/ansible.cfg
    - ansible-playbook sometask
  rules:
    - if: $CI_PIPELINE_SOURCE == "pipeline"
```
