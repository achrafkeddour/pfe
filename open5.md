Below is a **full command-by-command recipe** to deploy **MicroK8s + Open5GS** on **Ubuntu 22.04** on a single VM.

This is the **cleanest, most stable, easiest** Kubernetes setup for Open5GS.

---

# ✅ **Section 1 — Install MicroK8s**

```bash
sudo apt update
sudo apt install -y curl git net-tools

# Install MicroK8s
sudo snap install microk8s --classic

# Add your user to microk8s group
sudo usermod -aG microk8s $USER
sudo chown -f -R $USER ~/.kube

# Re-login to apply group change
newgrp microk8s

# Check cluster
microk8s status --wait-ready
```

---

# ✅ **Section 2 — Enable required MicroK8s add-ons**

```bash
microk8s enable dns
microk8s enable storage
microk8s enable metallb    # optional but helpful
microk8s enable multus
```

When Metallb asks for an address pool, use something inside your VM’s network.
Example for 192.168.122.x (KVM default):

```
192.168.122.240-192.168.122.250
```

---

# ✅ **Section 3 — Install Helm**

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

---

# ✅ **Section 4 — Clone the Open5GS Kubernetes repo**

We will use the well-maintained manifests repo:

```bash
git clone https://github.com/niloysh/open5gs-k8s.git
cd open5gs-k8s
```

---

# ✅ **Section 5 — Add Multus network configuration**

This repo includes two example networks.

Apply them:

```bash
kubectl apply -f multus/namespace.yaml
kubectl apply -f multus/multus-daemonset.yaml
kubectl apply -f multus/networks.yaml
```

(These create `n2network`, `n3network`, etc.)

---

# ✅ **Section 6 — Deploy MongoDB (Open5GS database)**

```bash
kubectl apply -f mongodb/mongodb-deployment.yaml
kubectl apply -f mongodb/mongodb-service.yaml
```

Check:

```bash
kubectl get pods -n open5gs
```

---

# ✅ **Section 7 — Deploy Open5GS Core Network Functions**

Apply everything:

```bash
kubectl apply -f open5gs/
```

This includes:

* NRF
* AMF
* SMF
* AUSF
* UDM
* UDR
* PCF
* UPF
* NSSF
* WebUI

Check status:

```bash
kubectl get pods -n open5gs -w
```

Wait until all pods show **Running**.

---

# ✅ **Section 8 — Access the Open5GS WebUI**

Expose via NodePort:

```bash
kubectl apply -f open5gs/webui-service.yaml
```

Get the port:

```bash
kubectl get svc -n open5gs | grep webui
```

You’ll see something like:

```
webui   NodePort  10.152.183.22   <none>   30080:30080/TCP
```

Open from your browser:

```
http://<your_VM_IP>:30080
```

Login credentials:

```
username: admin
password: 1423
```

---

# ✅ **Section 9 — Verify UPF networking**

Check UPF pod:

```bash
kubectl logs -n open5gs deploy/upf
```

You should see:

```
Initializing GTP devices
```

Make sure Linux kernel GTP module is present:

```bash
lsmod | grep gtp
```

Ubuntu 22.04 includes `gtp.ko` by default — no build needed.

---



