```
sudo apt-get update
sudo apt-get install -y curl apt-transport-https
```

# Download the latest stable kubectl binary
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

# Make it executable
```
chmod +x kubectl
```

# Move it into your PATH
```
sudo mv kubectl /usr/local/bin/kubectl
```

# Test the installation
```
kubectl version --client
```

# Install Minikube (local cluster)
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
# Start cluster (using Docker as backend)
```
minikube start --driver=docker
```
# Verify cluster is up
```
kubectl get nodes
```


# put the content of new files (inside k8s)
```
microservices-demo/
│
├── service-a/
├── service-b/
├── service-c/
├── docker-compose.yml
└── k8s/
    ├── namespace.yaml
    ├── service-a/
    │   ├── deployment.yaml
    │   └── service.yaml
    ├── service-b/
    │   ├── deployment.yaml
    │   └── service.yaml
    └── service-c/
        ├── deployment.yaml
        └── service.yaml

```

# Build & Load Images into Minikube 
```
cd ~/microservices-demo

eval $(minikube docker-env)

docker build -t service-a:latest ./service-a
docker build -t service-b:latest ./service-b
docker build -t service-c:latest ./service-c
```


# Deploy to Kubernetes
```
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/ -R -n microservices-demo
```

# Verify
```
kubectl get pods -n microservices-demo
kubectl get svc -n microservices-demo
```

# test full.. (hadi la commande ndirha f la VM directe , pas en ssh)
```
minikube service service-c -n microservices-demo
```

i check :   http://192.168.x.x:32749




✅ What this means technically:

Your Pods are running fine.

Services (ClusterIP and NodePort) are working.

DNS-based inter-service communication is working.

Load balancing is happening automatically (you could hit different replicas).

Kubernetes is now managing your 3-service microservice architecture without Docker Compose.
