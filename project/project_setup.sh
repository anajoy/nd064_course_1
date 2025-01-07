## prepapre second vagrant instance for project with following changes:
# config.vm.box = "opensuse/Leap-15.6.x86_64"
# config.vm.box_version = "15.6.13.356"
# config.vm.network "forwarded_port", guest: 3111, host: 3111
# config.vm.network "private_network", ip: "192.168.50.5"
# vb.name = "nd064_course_1_project"

## install kubectl (k3s)

curl -sfL https://get.k3s.io | sh -

kubectl version

# localhost:~ # kubectl version
# Client Version: v1.31.4+k3s1
# Kustomize Version: v5.4.2
# Server Version: v1.31.4+k3s1


## install argocd
# see https://argo-cd.readthedocs.io/en/stable/getting_started/#1-install-argo-cd
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl get po -n argocd
kubectl get svc -n argocd

# reconfigure argocd-server to connect over nodeport (and not cluster ip)
mkdir argocd
kubectl get svc -n argocd argocd-server -o yaml > argocd-nodeport.yaml

# remove already defined config and change to nodeport (file should look like project/argocd-nodeport.yaml)
# save file and apply change
vi argocd-nodeport.yaml
kubectl apply -f argocd-nodeport.yaml

# test access by browser url: http://192.168.50.5:30007

# install argocd CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

# create login account by following instructions in "create_selfsigned_localhost_certificates.sh"
# for details see folder project/localhost_ca
