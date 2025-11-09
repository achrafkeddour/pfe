Got it — let’s build this **from zero**, for a beginner, on **Ubuntu 22.04 VM (2 CPU / 4–5GB RAM)**.

👉 Therefore we’ll install the **minimum setup**:
**free5GC core only, running on a single Kubernetes minikube node using docker as its driver**.

Later you can add UERANSIM if your resources allow.

---

# ✅ Step-by-step, simplified, clean installation (beginner-friendly)

Copy/paste each block.

---

## **1️⃣ Update system**

```bash
sudo apt update
sudo apt upgrade -y
```

---

## **2️⃣ Install basic tools**

```bash
sudo apt install -y curl wget git vim apt-transport-https ca-certificates build-essential
```

---

## **3️⃣ Install gtp5g kernel module (required by free5GC)**

```bash
git clone https://github.com/free5gc/gtp5g.git
cd gtp5g
make
sudo make install
```

Confirm it loads:

```bash
lsmod | grep gtp
```

---

## **4️⃣ Install Docker (VERY IMPORTANT)**

Remove any old versions:

```bash
sudo apt remove docker docker.io containerd runc
```

Install:

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Enable/start:

```bash
sudo systemctl enable --now docker
```

Add yourself to docker group:

```bash
sudo usermod -aG docker $USER
```

⚠️ **Log out then log back in** (or reboot VM).

Test:

```bash
docker ps
```

---

## **5️⃣ Install kubectl**

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

---

## **6️⃣ Install minikube**

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## **7️⃣ Start minikube with LOW resource profile**

This is CRITICAL for your small VM.

```bash
minikube start --driver=docker --cpus=2 --memory=3500mb
```

Check status:

```bash
minikube status
```

---

## **8️⃣ Install Helm**

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

---

## **9️⃣ Install Multus CNI (required!)**

```bash
kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset.yml
```

Wait 20–30 seconds:

```bash
kubectl get pods -n kube-system
```

---

## **🔟 Deploy free5GC Helm charts**

Clone helm chart repo:

```bash
git clone https://github.com/Orange-OpenSource/towards5gs-helm
cd towards5gs-helm
```

Create namespace:

```bash
kubectl create namespace free5gc
```

Install core (light version):

```bash
helm install free5gc ./charts/free5gc --namespace free5gc
```

Wait for pods:

```bash
kubectl get pods -n free5gc
```

➡️ They MUST eventually be in **Running** or **Completed** state.

---

# ✅ What to do if pods don’t start

Use:

```bash
kubectl describe pod <pod-name> -n free5gc
```

Logs:

```bash
kubectl logs <pod-name> -n free5gc
```

---

# 🎯 That’s the minimal working setup

At this point you have:

* Kubernetes
* Multus
* Docker
* Minikube single node
* free5GC core deployed (AMF/UPF/SMF/AUSF/UDM/PCF/NSSF)

---

# ❤️ If you want, I can do “guided troubleshooting”

You just send me:

✅ output of:

```bash
kubectl get pods -n free5gc
```

and if any pod is not running,

```bash
kubectl logs <pod-name> -n free5gc
```

I’ll tell you EXACTLY what to fix.
