Vagrant.configure("2") do |config|
        config.vm.box = "Fedora-Cloud-Base-Vagrant-22-20150521.x86_64.vagrant-libvirt.box"
        config.vm.network :forwarded_port, guest: 80, host: 8008, auto_correct: true

        config.vm.synced_folder  "./guest", "/opt/ims", create: true, type: "rsync"

        config.vm.provider :libvirt do |domain|
                domain.memory = 2048
                domain.cpus = 2
                domain.storage :file, :size => '20G'
        end

        config.vm.provision "shell" do |s|
                s.inline = "/bin/sh -c '/opt/ims/provision.sh'"
        end
end
