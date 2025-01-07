## Install go

# Download and install https://go.dev/doc/install
# Download with browser and save file in dir with vagrant file: https://go.dev/dl/go1.23.4.linux-amd64.tar.gz

# Login to vagrant by commands below
vagrant status
vagrant up
vagrant reload
vagrant ssh
# change to user root
sudo su -

# change to mounted root dir on guest server
cd /vagrant
ls -l

rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> $HOME/.bashrc
