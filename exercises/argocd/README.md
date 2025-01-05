## Excercise chapter 5

### Configure vagrant
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

#### install argocd
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

#### define nodeport config

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

#### retrieve admin password (does not work anymore)
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name  |cut -d '/' -f 2

#### install TLS certificate
curl -L -o kubectl-cert-manager.tar.gz https://github.com/cert-manager/cert-manager/releases/download/v1.5.5/kubectl-cert_manager-linux-amd64.tar.gz
tar xzf kubectl-cert-manager.tar.gz
mv kubectl-cert_manager /usr/local/bin

#### selfsigned certificiate
kubectl cert-manager create certificaterequest my-sandbox-tls-cr --from-certificate-file  --fetch-certificate --timeout 20m

kubectl cert-manager create certificaterequest my-sandbox-1-tls-cr --from-certificate-file selfsigned-issuer-root-ca.yaml sandbox-1-tls.yaml --fetch-certificate --timeout 20m

mkdir .ssh
ssh-keygen -b 2048 -t ed25519 -n argocd
chmod 700 .ssh

kubectl create -n argocd secret tls argocd-server-tls \
  --cert=/root/.ssh/id_ed25519.pub
  --key=/root/.ssh/id_ed25519

#### workaround by installing argocd CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

### create login account by following instructions in "create_selfsigned_localhost_certificates.sh"

### Deploy applications to argocd: step 1: deploy crd file to argocd. Application configured is in state unsynced.
#### application nginx
kubectl apply -f argocd-nginx.yaml
kubectl get po -n demo
#### sync manually by pressing butting after opening application.
kubectl get po -n demo

#### application python
kubectl apply -f argocd-python.yaml
kubectl get po -n default
#### show all pods: python is running on node default
kubectl get po -A

#### access over localhost:
kubectl port-forward pod/python-helloworld-86687555f9-7dxwh 5111:5000
#### portforwarding did not work for nginx (8111) or python (5000) app
kubectl get svc -n default -o wide
#### Corrected by adding more ports to vagrant config:
  config.vm.network "forwarded_port", guest: 5111, host: 5000
  config.vm.network "forwarded_port", guest: 8111, host: 8111
  config.vm.network "forwarded_port", guest: 443, host: 443
  config.vm.network "forwarded_port", guest: 80, host: 80


### deploying python helloworld and nginx-alpine with helm charts
#### delete apps to start from scratch
kubectl delete all --all -n default --force
kubectl delete all --all -n demo --force

#### adapt and deploy helm charts to argocd
cd exercises/argocd/exercise_3
kubectl apply -f argocd-helm-python-prod.yaml
kubectl apply -f argocd-helm-python.yaml
kubectl apply -f argocd-helm-nginx-staging.yaml
kubectl apply -f argocd-helm-nginx-prod.yaml

#### check for deployed resorces:
kubectl get ns

localhost:/vagrant/argocd/exercise_3 # kubectl get ns
NAME              STATUS   AGE
argocd            Active   14d
cert-manager      Active   13d
default           Active   56d
kube-node-lease   Active   56d
kube-public       Active   56d
kube-system       Active   56d
prod              Active   83m
staging           Active   81m
test              Active   84m
test-udacity      Active   56d

kubectl get deploy -n staging
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-alpine   1/1     1            1           84m

kubectl get deploy -n prod
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
nginx-alpine        2/2     2            2           82m
python-helloworld   3/3     3            3           86m

kubectl get svc -n staging
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
nginx-alpine   ClusterIP   10.43.187.153   <none>        8111/TCP   86m

kubrctl get svc -n prod
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
nginx-alpine   ClusterIP   10.43.109.108   <none>        80/TCP    85m

kubectl get cm -n staging -o yaml

#### Output example
kubectl get cm -n prod -o yaml
apiVersion: v1
items:
- apiVersion: v1
  data:
    ca.crt: |
      -----BEGIN CERTIFICATE-----
      MIIBdjCCAR2gAwIBAgIBADAKBggqhkjOPQQDAjAjMSEwHwYDVQQDDBhrM3Mtc2Vy
      dmVyLWNhQDE3MzEyNTQxODQwHhcNMjQxMTEwMTU1NjI0WhcNMzQxMTA4MTU1NjI0
      WjAjMSEwHwYDVQQDDBhrM3Mtc2VydmVyLWNhQDE3MzEyNTQxODQwWTATBgcqhkjO
      PQIBBggqhkjOPQMBBwNCAASfmscliEI1pi3a4mSzFdzR1d1ojmc4KBtt2gIuhl84
      s/yuCLcxDxb1xUGUcwufDbLuto5zhl9s3asNKJwN53zTo0IwQDAOBgNVHQ8BAf8E
      BAMCAqQwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUPM9pUhPDoqbcn+nSnTE3
      /k3EIdEwCgYIKoZIzj0EAwIDRwAwRAIgOOEM7bQ/u9Cr41QgRx9IOA5by1YCaMAp
      40FHoflP6v8CIAI3EMEmIHZCbbo4jybfIwpO0duo/2N4+JbSAn6hF4Fl
      -----END CERTIFICATE-----
  kind: ConfigMap
  metadata:
    annotations:
      kubernetes.io/description: Contains a CA bundle that can be used to verify the
        kube-apiserver when using internal endpoints such as the internal service
        IP or kubernetes.default.svc. No other usage is guaranteed across distributions
        of Kubernetes clusters.
    creationTimestamp: "2025-01-05T19:33:50Z"
    name: kube-root-ca.crt
    namespace: prod
    resourceVersion: "31705"
    uid: c3dc5800-eb4f-47e2-ab37-df7734243edc
- apiVersion: v1
  data:
    version: 1.17.0
  kind: ConfigMap
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"v1","data":{"version":"1.17.0"},"kind":"ConfigMap","metadata":{"annotations":{},"labels":{"app.kubernetes.io/instance":"nginx-prod"},"name":"nginx-version","namespace":"prod"}}
    creationTimestamp: "2025-01-05T19:37:32Z"
    labels:
      app.kubernetes.io/instance: nginx-prod
    name: nginx-version
    namespace: prod
    resourceVersion: "31891"
    uid: 56b24afa-a758-43a0-b8fa-19b7437f549c
kind: List
metadata:
  resourceVersion: ""
