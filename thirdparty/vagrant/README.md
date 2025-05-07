## Vagrant setup

- Have a setup DATA directory
```
export VAGRANT_DATA_DIR="/tmp/vagrant"
```

- Setup correct box

```
vagrant box remove rockylinux/9 --provider virtualbox
vagrant box add rockylinux/9 --provider virtualbox
```

- Run using a config file
```
VAGRANT_VAGRANTFILE=thirdparty/vagrant/splunk_standalone.Vagrantfile vagrant up
```

- Destroy
```
VAGRANT_VAGRANTFILE=thirdparty/vagrant/splunk_standalone.Vagrantfile vagrant destroy -f
```