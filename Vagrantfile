# -*- mode: ruby -*-
# vi: set ft=ruby :
default_box = "generic/opensuse42"

Vagrant.configure("2") do |config|

  config.vm.define "master" do |master|
    master.vm.box = default_box
    master.vm.hostname = "master"
    master.vm.network 'private_network', ip: "192.168.50.4"
    master.vm.provider "virtualbox" do |v|
      v.memory = "3072"
      v.name = "master"
      end
    master.vm.provision "file", source: "./argocd", destination: "$HOME/argocd"
    master.vm.provision "shell", inline: <<-SHELL
    sudo zypper --non-interactive install apparmor-parser
    curl -sfL https://get.k3s.io | sh -
    SHELL
  end

end
