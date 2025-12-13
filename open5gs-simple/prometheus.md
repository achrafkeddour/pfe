## 1. install 
```bash
# Install Prometheus
cd ~
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64

# Create Prometheus config
nano prometheus2.yml

# Avoid 9090
./prometheus   --config.file=prometheus2.yml   --web.listen-address=:9091

```


