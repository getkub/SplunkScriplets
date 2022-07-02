```
docker pull joniator/ansible:latest


docker run -it --name=test_ansible joniator/ansible:latest /bin/sh
docker stop test_ansible && docker rm $(docker ps -qa)
```