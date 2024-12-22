PS D:\repo\udacity\nd064_course_1\exercises> vagrant up
==> vagrant: A new version of Vagrant is available: 2.4.3 (installed version: 2.4.2)!
==> vagrant: To upgrade visit: https://www.vagrantup.com/downloads.html

Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'opensuse/Leap-15.2.x86_64' version '15.2.31.632' is up to date...
==> default: Resuming suspended VM...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
==> default: Machine booted and ready!
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
PS D:\repo\udacity\nd064_course_1\exercises> vagrant ssh
Last login: Sun Nov 10 21:21:28 2024 from 10.0.2.2
Have a lot of fun...

vagrant@localhost:~> sudo su -

localhost:~ # kubectl get nodes
NAME        STATUS   ROLES                  AGE   VERSION
localhost   Ready    control-plane,master   42d   v1.30.6+k3s1

localhost:~ # kubectl get po -A
NAMESPACE      NAME                                      READY   STATUS      RESTARTS   AGE
demo           nginx-alpine-c6db5d794-29phr              1/1     Running     0          41d
demo           nginx-alpine-c6db5d794-mq5vr              1/1     Running     0          41d
demo           nginx-alpine-c6db5d794-rc5ll              1/1     Running     0          41d
kube-system    coredns-7b98449c4-f9bn9                   1/1     Running     0          42d
kube-system    helm-install-traefik-crd-wgbfh            0/1     Completed   0          42d
kube-system    helm-install-traefik-mrdbc                0/1     Completed   1          42d
kube-system    local-path-provisioner-595dcfc56f-88g9c   1/1     Running     0          42d
kube-system    metrics-server-cdcc87586-r9r5c            1/1     Running     0          42d
kube-system    svclb-traefik-92eb4115-blbt8              2/2     Running     0          42d
kube-system    traefik-d7c9c5778-l57wb                   1/1     Running     0          42d
test-udacity   go-helloworld-59fdcb6685-k4smn            1/1     Running     0          41d
test-udacity   go-helloworld-59fdcb6685-q52gw            1/1     Running     0          41d
test-udacity   go-helloworld-59fdcb6685-tdvq5            1/1     Running     0          41d

# install argocd
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl get po -n argocd
kubectl get svc -n argocd

localhost:~ # kubectl get svc -n argocd
NAME                                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
argocd-applicationset-controller          ClusterIP   10.43.129.104   <none>        7000/TCP,8080/TCP            2m35s
argocd-dex-server                         ClusterIP   10.43.105.74    <none>        5556/TCP,5557/TCP,5558/TCP   2m35s
argocd-metrics                            ClusterIP   10.43.98.169    <none>        8082/TCP                     2m35s
argocd-notifications-controller-metrics   ClusterIP   10.43.203.224   <none>        9001/TCP                     2m34s
argocd-redis                              ClusterIP   10.43.36.176    <none>        6379/TCP                     2m34s
argocd-repo-server                        ClusterIP   10.43.123.107   <none>        8081/TCP,8084/TCP            2m34s
argocd-server                             ClusterIP   10.43.16.212    <none>        80/TCP,443/TCP               2m34s
argocd-server-metrics                     ClusterIP   10.43.134.172   <none>        8083/TCP                     2m34s


 kubectl get svc -n argocd argocd-server -o yaml > argocd-nodeport.yaml

 vi argocd-nodeport.yaml

 ## define nodeport config

localhost:~ # kubectl apply -f argocd-nodeport.yaml
service/argocd-server-nodeport created

localhost:~ # kubectl get svc -n argocd
NAME                                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
argocd-applicationset-controller          ClusterIP   10.43.129.104   <none>        7000/TCP,8080/TCP            36m
argocd-dex-server                         ClusterIP   10.43.105.74    <none>        5556/TCP,5557/TCP,5558/TCP   36m
argocd-metrics                            ClusterIP   10.43.98.169    <none>        8082/TCP                     36m
argocd-notifications-controller-metrics   ClusterIP   10.43.203.224   <none>        9001/TCP                     36m
argocd-redis                              ClusterIP   10.43.36.176    <none>        6379/TCP                     36m
argocd-repo-server                        ClusterIP   10.43.123.107   <none>        8081/TCP,8084/TCP            36m
argocd-server                             ClusterIP   10.43.16.212    <none>        80/TCP,443/TCP               36m
argocd-server-metrics                     ClusterIP   10.43.134.172   <none>        8083/TCP                     36m
argocd-server-nodeport                    NodePort    10.43.128.71    <none>        80:30007/TCP,443:30008/TCP   69s

# retrieve admin password (does not work anymore)
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name  |cut -d '/' -f 2

# workaround by installing argocd CLI