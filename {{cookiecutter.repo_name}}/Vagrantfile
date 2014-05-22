$setup = <<SCRIPT
    DEBIAN_FRONTEND=noninteractive apt-get update
SCRIPT

$dependencies = <<SCRIPT
    DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql libpq-dev
    DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev libjpeg-dev zlib1g-dev
    DEBIAN_FRONTEND=noninteractive apt-get install -y python-virtualenv virtualenvwrapper
SCRIPT

Vagrant.configure('2') do |config|

    config.vm.box = 'precise64'
    config.vm.box_url = "http://files.vagrantup.com/" + config.vm.box + ".box"

    config.ssh.forward_agent = true
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 8000, guest: 8000

    config.vm.provision "shell", inline: $setup
    config.vm.provision "shell", inline: $dependencies
end
