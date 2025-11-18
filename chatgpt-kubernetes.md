Nice — you already did a lot of the hard work (Docker + `gtp5g` build). Below is a **compact, structured, copy-pasteable plan (with all commands)** to move from a fresh Ubuntu 22.04 VM → single-node Kubernetes → free5GC running in Kubernetes (Core + UPF) + a simulated RAN (UERANSIM) for testing. I keep it short, actionable and focused on the minimal reliable path: **MicroK8s (single-node) + Helm + free5gc-helm charts**. I’ll also call out the few things you already did and key gotchas. Wherever the approach relies on upstream docs or charts I’ll cite them.

Top references (for the commands below): free5gc Helm charts and official guide, community deploy notes + recent multi-node guide. ([GitHub][1])

---

# Goal (one line)

Single Ubuntu 22.04 VM → MicroK8s single-node cluster with free5GC (core NFs) + UPF (using host GTP module), deploy UERANSIM to test end-to-end.

---

# Quick checklist (what you need on the VM)

* Ubuntu 22.04 (you have)
* Docker installed & running (you already installed).
* Kernel headers / ability to build/load `gtp5g` (you already built it earlier).
* At least 4-8 GB RAM and 2+ vCPUs for reasonable tests.

---

# Full step-by-step (copy/paste commands)

> Note: run each command in sequence. Commands that need `sudo` are marked. Replace `<your-user>` with your username only where needed.

### 0. (Optional) Re-run verified prerequisites (safe to run again)

```bash
# update + essentials (you already ran this but safe)
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential dkms linux-headers-$(uname -r) curl ca-certificates gnupg lsb-release
```

### 1. Ensure the gtp5g module is built & loaded on this node

You already did this previously, but verify kernel module is present and enabled now (must match running kernel).

```bash
# check module loaded
lsmod | grep gtp5g || echo "gtp5g not loaded"

# if not loaded, build & install as you did:
cd /tmp
git clone https://github.com/free5gc/gtp5g.git
cd gtp5g
make
sudo make install
sudo modprobe gtp5g

# confirm
lsmod | grep gtp5g
```

*(UPF pods will need the Linux kernel module available on the host)*. ([free5gc.org][2])

### 2. Install microk8s (single-node k8s) and enable required addons

MicroK8s is easiest for single VM labs and has a Helm3 addon. We’ll enable `flannel` (simpler for UPF IP forwarding) and `multus` if you plan multiple interfaces later.

```bash
# install snapd if needed, then microk8s
sudo snap install microk8s --classic

# add your user to microk8s group (log out / log in or run newgrp)
sudo usermod -a -G microk8s $USER
newgrp microk8s

# check kubectl via microk8s
microk8s kubectl get nodes

# enable basic addons
microk8s enable dns storage helm3 ingress

# enable CNI suited for free5GC (flannel recommended for simpler IP forwarding)
microk8s enable flannel
# (optional) enable multus if you will attach secondary interfaces to pods:
microk8s enable multus
```

Free5GC guides recommend careful CNI configuration — many community guides use Flannel to avoid Calico IP-forward tweaks. ([free5gc.org][3])

### 3. Make kernel network settings expected by UPF / host

```bash
# enable IP forwarding and other typical settings
sudo tee /etc/sysctl.d/99-free5gc.conf > /dev/null <<EOF
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
net.netfilter.nf_conntrack_max=262144
EOF
sudo sysctl --system
```

### 4. Ensure Docker is available to microk8s or use containerd (microk8s has containerd)

(You already have Docker; microk8s uses containerd internally — fine. Make sure docker services are running if you want to build images locally.)

```bash
sudo systemctl status docker
```

### 5. Install Helm (if not enabled via microk8s helm3 addon)

If you enabled `microk8s enable helm3` you can use `microk8s helm3`. Otherwise:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod +x get_helm.sh
./get_helm.sh
```

### 6. Prepare namespace, clone charts

Use the official free5gc helm repo or community charts (free5gc-helm). Example uses the free5gc-helm repo (single-click charts). ([GitHub][1])

```bash
# create namespace
microk8s kubectl create namespace free5gc

# clone official helm charts (or add a chart repo)
git clone https://github.com/free5gc/free5gc-helm.git ~/free5gc-helm
cd ~/free5gc-helm
```

### 7. Edit `values.yaml` minimally (network interfaces and UPF N6)

Open `values.yaml` (or the specific chart values for `free5gc` & `upf`) and set these minimal parameters to match the VM host interface that connects to the data network (e.g. `ens3`, `eth0`, `ens18` etc). Example fields you’ll typically change:

```yaml
# (example snippet - adjust file, or create my-values.yaml)
global:
  n2network:
    masterIf: "ens3"
  n3network:
    masterIf: "ens3"
  n4network:
    masterIf: "ens3"
  n6network:
    masterIf: "ens3"
    subnetIP: "192.168.100.0"
    gatewayIP: "192.168.100.1"
    cidr: "24"

free5gc-upf:
  upf:
    n6if:
      ipAddress: "192.168.100.2"
```

Create `my-values.yaml` and edit to match your interface names and chosen N6 subnet. (The charts rely on you mapping Kubernetes pods to host interfaces). See chart docs for exact field names. ([GitHub][1])

### 8. Deploy free5GC core + UPF with Helm

(Use `microk8s helm3` or `helm` depending on install.)

```bash
# from ~/free5gc-helm or where chart is present
# install core (example chart name may be free5gc or free5gc-core; check repo)
microk8s helm3 install free5gc ./charts/free5gc -n free5gc -f my-values.yaml

# install UPF chart (some repos keep UPF separate)
microk8s helm3 install free5gc-upf ./charts/free5gc-upf -n free5gc -f my-values.yaml
```

If the repo is packaged as a single chart, there will be instructions in its README; adapt the helm command accordingly. ([GitHub][1])

### 9. Make sure UPF pods can use host `gtp5g`

UPF must be able to talk to the host GTP stack or run privileged mode / hostNetwork. Many charts run UPF as a DaemonSet or privileged pod with `hostNetwork: true` and device access. If your chart doesn't, patch it: set `securityContext: privileged: true` and `hostNetwork: true` in UPF deployment values and mount `/lib/modules` to the pod. Example (values):

```yaml
upf:
  hostNetwork: true
  securityContext:
    privileged: true
  hostPathMounts:
    - hostPath: /lib/modules
      mountPath: /lib/modules
```

Also make sure `gtp5g` is modprobed on the host (see step 1).

**Important:** the UPF pod may need CAP_NET_ADMIN and NET_RAW; the chart docs explain these fields. ([HackMD][4])

### 10. Deploy UERANSIM (gNB + UE) for testing

Community helm charts or manifests exist; simpler: clone a repo with k8s manifests for UERANSIM and deploy into `free5gc` namespace:

```bash
cd ~
git clone https://github.com/free5gc/free5gc-helm.git ueransim-demo  # or use a community ueransim k8s repo
# (If using a repo with ueransim manifests)
microk8s kubectl apply -f ueransim-k8s/ueransim-gnb.yaml -n free5gc
microk8s kubectl apply -f ueransim-k8s/ueransim-ue.yaml -n free5gc
```

If you prefer to run UERANSIM locally on VM (outside cluster), you can run it locally and connect N2/N3 to the core. Community guides show both ways. ([GitHub][5])

### 11. Verify & debug

```bash
# check pods
microk8s kubectl -n free5gc get pods -o wide

# logs (example for AMF)
microk8s kubectl -n free5gc logs deploy/amf -f

# check UPF logs
microk8s kubectl -n free5gc logs deploy/upf -f

# port-forward WebUI (if chart exposes it on 5000)
microk8s kubectl -n free5gc port-forward svc/free5gc-webui 5000:5000 &
# then open: http://localhost:5000  (admin/free5gc default creds in many examples)
```

If pods crash: `kubectl describe pod <pod>` and `kubectl logs` will point to missing host mounts, insufficient privileges, or network misconfiguration.

---

# Minimal `my-values.yaml` example

(Adjust interface and IPs to your host; this is illustrative — paste into `my-values.yaml` and adjust)

```yaml
global:
  n2network:
    masterIf: "ens3"
  n3network:
    masterIf: "ens3"
  n4network:
    masterIf: "ens3"
  n6network:
    masterIf: "ens3"
    subnetIP: "192.168.100.0"
    gatewayIP: "192.168.100.1"
    cidr: "24"

free5gc-upf:
  upf:
    hostNetwork: true
    n6if:
      ipAddress: "192.168.100.2"
    securityContext:
      privileged: true
    hostPathMounts:
      - hostPath: /lib/modules
        mountPath: /lib/modules
```

---

# Common gotchas & quick fixes

* **Kernel mismatch:** `gtp5g` must be built against the running kernel headers. If pods say device not found, rebuild module. ([free5gc.org][2])
* **CNI (Calico vs Flannel):** Calico requires extra changes for IP forwarding; for a single VM lab, Flannel is simpler. If you use Calico you may need to edit the Calico CNI to allow host IP forwarding (see free5gc guide). ([free5gc.org][3])
* **UPF privileges:** UPF pods commonly require `hostNetwork: true`, privileged container, and host `/lib/modules` mounted. If UPF cannot attach the GTP socket, check privileges and `lsmod`. ([HackMD][4])
* **Interface names:** make absolutely sure the interface in `values.yaml` is the host interface that actually carries the data plane (run `ip addr` to confirm). ([HackMD][4])

---

# Test the data path (once everything is running)

1. Start UERANSIM UE/gNB (in cluster or local) and watch AMF, SMF logs for registration and PDU session.
2. From within the UPF node (or a pod with `hostNetwork`), `ping` an assigned UE IP via N6 to verify user plane.
3. Use `kubectl exec -n free5gc -it <ue-pod> -- ping 8.8.8.8` (if routing/NAT done) or `iperf` for throughput tests.

---

# If you want a smaller/faster path

* For first experiments, keep core (AMF/SMF/UPF) in Kubernetes using the Helm charts and run UERANSIM locally on your VM (not in K8s) — simpler to debug NGAP/N3 connectivity. Many community posts follow this pattern. ([HackMD][6])

---

# Useful links (for deeper reads / exact chart fields)

* free5gc-helm (official helm charts + README): ([GitHub][1])
* free5gc user guide and install notes (CNI / kernel / UPF tips): ([free5gc.org][2])
* recent multi-node Helm deployment guide (2025): ([free5gc.org][7])
* community examples / manifests (uetansim + k8s examples): ([GitHub][5])

---

If you want, I can now:

* generate a ready-to-apply `my-values.yaml` tuned to **your VM** interface names and a chosen N6 subnet (tell me your `ip addr` output or the interface name and an IP you want for UPF), **or**
* produce exact `kubectl apply` manifests for UPF with the privileged settings if your chosen chart lacks them.

Which of those two would you like next? (If you want the `my-values.yaml` I will produce it immediately from the interface/name you give — no waiting.)

[1]: https://github.com/free5gc/free5gc-helm?utm_source=chatgpt.com "Helm charts for deploying free5GC on Kubernetes"
[2]: https://free5gc.org/guide/?utm_source=chatgpt.com "User Guide"
[3]: https://free5gc.org/guide/7-free5gc-helm/?utm_source=chatgpt.com "free5gc-helm"
[4]: https://hackmd.io/LVyfZDcUTD-b17vxkxnOaw?utm_source=chatgpt.com "Deployment with Free5GC, Kubernetes and Helm"
[5]: https://github.com/niloysh/free5gc-k8s?utm_source=chatgpt.com "niloysh/free5gc-k8s: 5G core deployment using ..."
[6]: https://hackmd.io/%40haidinhtuan/ryRuKdEI3?utm_source=chatgpt.com "Deployment with Free5GC, Kubernetes and Helm"
[7]: https://free5gc.org/blog/20250416/20250416/?utm_source=chatgpt.com "A Multi-Node Helm Deployment Approach"
