## run this command on your wsl2 instance in directory D:\repo\udacity\nd064_course_1\project\localhost_ca
# for details see: https://stackoverflow.com/a/67614862/28897488

openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")


## start your vagrant instance and change to root shell
PS D:\repo\udacity\nd064_course_1\project\argocd> vagrant up
PS D:\repo\udacity\nd064_course_1\project\argocd> vagrant ssh

localhost:~ # cd /vagrant/project/localhost_ca
ls -l localhost*
-rw-r--r-- 1 vagrant vagrant 1123 Dec 31 16:42 localhost.crt
-rw-r--r-- 1 vagrant vagrant 1704 Dec 31 16:42 localhost.key


kubectl create -n argocd secret tls argocd-server-tls \
  --cert=/vagrant/localhost_ca/localhost.crt \
  --key=/vagrant/localhost_ca/localhost.key

# install argocd client:
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

# define your kubectl env for argocd and reload your env file
vi .bashrc
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

argocd admin initial-password -n argocd

# This password must be only used for first time login. We strongly recommend you update the password using `argocd account update-password`.
## save the pw created to your password manager
