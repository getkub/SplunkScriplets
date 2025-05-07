Vagrant.configure("2") do |config|
  # Set custom data directory for Vagrant
  data_dir = ENV['VAGRANT_DATA_DIR'] || File.expand_path("~/vagrant_data")
  ENV['VAGRANT_HOME'] = data_dir
  
  # Enable debugging
  config.vm.boot_timeout = 600
  config.vm.graceful_halt_timeout = 600
  
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "rockylinux/9"
  config.vm.box_version = "5.0.0"
  config.vm.hostname = "splunk01"
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 9997, host: 9997, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8089, host: 8089, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 9887, host: 9887, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 514, host: 10514, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.network "private_network", type: "dhcp" 
  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
    vb.memory = "4096"  # Increased memory for better performance
    vb.cpus = 2         # Added CPU cores
    vb.name = "splunk-standalone"  # Custom VM name
    
    # Basic VirtualBox settings
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
    vb.customize ["modifyvm", :id, "--rtcuseutc", "on"]
    vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
    vb.customize ["modifyvm", :id, "--nested-hw-virt", "on"]
    vb.customize ["modifyvm", :id, "--vtx-vpid", "on"]
    vb.customize ["modifyvm", :id, "--vtxux", "on"]
    vb.customize ["modifyvm", :id, "--largepages", "on"]
    vb.customize ["modifyvm", :id, "--chipset", "ich9"]
    vb.customize ["modifyvm", :id, "--firmware", "efi"]
    vb.customize ["modifyvm", :id, "--graphicscontroller", "vboxsvga"]
    vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
    vb.customize ["modifyvm", :id, "--accelerate2dvideo", "on"]
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    # Update system
    dnf update -y
    
    # Install required dependencies
    dnf install -y wget curl net-tools
    
    # Set timezone
    timedatectl set-timezone UTC
    
    # Disable SELinux (optional, but often needed for Splunk)
    setenforce 0
    sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
    
    # Create Splunk user and group
    groupadd splunk
    useradd -g splunk -d /opt/splunk splunk
    
    # Create necessary directories
    mkdir -p /opt/splunk
    chown -R splunk:splunk /opt/splunk
  SHELL
end
