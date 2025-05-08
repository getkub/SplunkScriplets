## Various Splunk download automation
- Download Splunk and Universal forwarder
```
# for Ubuntu Linux VMs on MacOS
bash ./getSplunk.sh -p uf -v 9.4.2 -k deb -h e9664af3d956 -a arm64 -o linux

# for Ubuntu Linux VMs on Traditional OS
bash ./getSplunk.sh -p uf -v 9.4.2 -k deb -h e9664af3d956 -a amd64 -o linux
```