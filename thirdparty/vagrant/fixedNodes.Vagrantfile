# vagrant global-status --prune
# vagrant global-status
# vagrant up --provider virtualbox
# vagrant destroy -f ${id}
# vagrant box list
N = 2
nodes = [
  { :hostname => 'df1',  :ip => '192.168.0.42', :box => 'centos/7' },
  { :hostname => 'df2',  :ip => '192.168.0.43', :box => 'centos/7', :ram => 512 }
]

Vagrant.configure("2") do |config|
  nodes.each do |node|
    config.vm.define node[:hostname] do |nodeconfig|
      nodeconfig.vm.box = "centos/7"
      nodeconfig.vm.hostname = node[:hostname] + ".box"
      nodeconfig.vm.network :private_network, ip: node[:ip]
      memory = node[:ram] ? node[:ram] : 256;
      nodeconfig.vm.provider :virtualbox do |vb|
        vb.customize [
          "modifyvm", :id,
          "--cpuexecutioncap", "50",
          "--memory", memory.to_s,
        ]
      end
    end
  end
end
