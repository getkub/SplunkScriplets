# FreeBSD Vagrant
Vagrant.configure("2") do |config|
  config.vm.box = "freebsd/FreeBSD-11.2-RELEASE"
  config.vm.guest = :freebsd
  config.ssh.shell = "sh"
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true
  config.vm.box_version = "2018.06.22"
end
