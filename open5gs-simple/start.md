## 1. installation du open5gs
```bash
sudo apt install git build-essential meson ninja-build cmake flex bison \
libmnl-dev libyaml-dev libmicrohttpd-dev libcurl4-gnutls-dev libtins-dev \
libidn11-dev libmongoc-dev libbson-dev libnghttp2-dev libtalloc-dev \
libgcrypt20-dev libsctp1 libsctp-dev lksctp-tools
```

## 2. clone
```bash
cd ~
git clone https://github.com/open5gs/open5gs
cd open5gs
```

## 3. Compiler
```bash
meson build --prefix=`pwd`/install
ninja -C build
ninja -C build install
# À ce stade, tes binaires et configs sont dans ~/open5gs/install.
```

## 4. mongodb
```bash
  sudo apt install curl
  curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
  echo "deb [signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] \
https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
  sudo apt update
  sudo apt install -y mongodb-org
  sudo systemctl start mongod
  sudo systemctl enable mongod
  sudo systemctl status mongod
```


## 5. configuration de 5GC
- utilise les deux chemins
- 1. ```cd open5gs/install/bin```
  2. ```cd open5gs/install/etc``` 



