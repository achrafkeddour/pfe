# 1. verify 
```
uname -r
grep avx /proc/cpuinfo || true
```


# 2. 
```
sudo apt update
sudo apt upgrade -y

# essential tools
sudo apt install -y git build-essential dkms linux-headers-$(uname -r) curl ca-certificates gnupg lsb-release
```

# 3. Install Docker Engine + Docker Compose plugin (v2)
```
# add Docker's official GPG key and repository (official instructions)
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# allow your user to run docker without sudo (optional, log out/in required)
sudo usermod -aG docker $USER
newgrp docker
```

# 4. 
```
docker version
docker compose version
```
# 5. Install the gtp5g kernel module (required by UPF)
```
cd /tmp
git clone https://github.com/free5gc/gtp5g.git
cd gtp5g

# optional: checkout a stable tag if you want e.g. `v0.9.5` (check releases)
# git checkout v0.9.5

# build
make

# install (this will copy to /lib/modules and/or register dkms)
sudo make install

# load module now
sudo modprobe gtp5g

# confirm module is loaded
lsmod | grep gtp5g

```
# 6 Clone free5gc-compose and run prebuilt images (fastest)
```
cd ~
git clone https://github.com/free5gc/free5gc-compose.git
cd free5gc-compose

# pull images from Docker Hub
docker compose pull
```

----

```
# start everything (foreground)
# docker compose up
# OR run in background (recommended)
docker compose up -d

```

# 7
```
docker compose ps
```


# check 
```
http://localhost:5000
username: admin
password: free5gc
```


