# 1 install docker 

sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y
sudo usermod -aG docker $USER
newgrp docker

# 2 install and run rancher

```
docker run -d --restart=unless-stopped   --name rancher-server   --privileged   -p 80:80 -p 443:443   rancher/rancher:latest
```
then 
```
docker ps
docker logs container-ID  2>&1 | grep "Bootstrap Password:"
```

#### you can see the result in localhost
