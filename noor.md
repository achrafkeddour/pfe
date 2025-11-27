everything in my real machine that contains ubuntu 22.04


# 1. Container Runtime (Docker/containerd/CRI-O) .. and we choose Docker because Rancher + Kind rely on it smoothly




# 2. A tool to create/manage the Kubernetes cluster (Rancher / Minikube / kind / Microk8s)
....we choose Rancher , then open in browser: https://<your_vm_ip>




# 3. Rancher manages clusters, but you need to deploy a cluster to run the 5G core.
....we choose RKE2 (Rancher Kubernetes Engine v2) as our the Kubernetes Cluster (inside Rancher)




# 4. Kubernetes Add-ons Needed for 5G :
	A. CNI Plugin (Networking) , we choose Calico
	B. Ingress Controller , we choose NGINX Ingress
	C. Storage , we choose Longhorn (while we need persistence (UDR, MongoDB, logs) )




# 5. 5G Core Software Options (we choose Open5GS)


Install Open5GS : Kubernetes deployment (Clone the Helm/K8s charts , Then deploy)



#  6. UE + gNB Simulator (we choose UERANSIM)



# 7. Monitoring Tools : I heard that Rancher can deploy Prometheus/Grafana with one click so i prefer them 



# 🧪 8. Test Scenarios (as performed in the thesis)
Required Components

Multiple Kubernetes nodes (optional)

Open5GS running as pods

UERANSIM gNB + UE
	
Monitoring stack

Tests

Pod Failure & Self-Healing

Scaling UPF/AMF/SMF

Smart City Scenario (1000s of UE simulated)

