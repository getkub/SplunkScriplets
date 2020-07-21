# vagrant global-status --prune
# vagrant global-status
# vagrant up --provider virtualbox
# vagrant destroy -f ${id}
# vagrant global-status | grep df | cut -d' ' -f1| while read line; do vagrant destroy -f $line; done
# vagrant global-status | awk '/running/{print $1}' | xargs -r -d '\n' -n 1 -- vagrant suspend
# vagrant box list
BASE_NW_INTERFACE="ens160"
HOSTNAME_TAG="df"
BOX_RAM_MB = "2048"
BOX_CPU_COUNT = "2"


Vagrant.configure(2) do |config|
       # Specifying the box we wish to use
       config.vm.box = "centos/7"
       # Default port ranges are 2200 to 2250. You can change here if you need
       config.vm.usable_port_range = 2200..2250
       config.vm.network "public_network", bridge: BASE_NW_INTERFACE
       # Iterating the loop for 4 times and will create 4 VM nodes
       (1..4).each do |i|
       config.vm.hostname = "df-node#{i}"
       config.vm.define "df-node#{i}" do |node|
       node.vm.provider :virtualbox do |virtualbox|
           virtualbox.customize ["modifyvm", :id, "--memory", BOX_RAM_MB]
     	   virtualbox.customize ["modifyvm", :id, "--cpus", BOX_CPU_COUNT]
       end
       end
       end
end

