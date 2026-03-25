# Vagrantfile - Lightweight Elastic Agent testing setup

Vagrant.configure("2") do |config|
  # Default VirtualBox provider settings
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"  # Minimal RAM
    vb.cpus = 1        # Single CPU
    vb.gui = false     # Headless for speed
  end

  # AlmaLinux 9 VMs
  (1..3).each do |i|
    config.vm.define "almalinux-test#{i}" do |vm|
      vm.vm.box = "almalinux/9"       # Minimal AlmaLinux 9 box
      vm.vm.hostname = "almalinux-test#{i}"

      # Host-only network for stable IP
      vm.vm.network "private_network", ip: "192.168.56.1#{i}"

      # Optional: bridged network for internet access
      # vm.vm.network "public_network"
    end
  end

  # Ubuntu 24.04 minimal VMs
  (1..2).each do |i|
    config.vm.define "ubuntu-test#{i}" do |vm|
      vm.vm.box = "generic/ubuntu2404" # Minimal Ubuntu 24.04 box
      vm.vm.hostname = "ubuntu-test#{i}"

      # Host-only network for stable IP
      vm.vm.network "private_network", ip: "192.168.56.2#{i}"

      # Optional: bridged network for internet access
      # vm.vm.network "public_network"
    end
  end
end
