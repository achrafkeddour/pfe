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

## 4.2 second solution for mongodb
```bash
# Create a temporary directory
mkdir ~/mongodb-packages
cd ~/mongodb-packages

# Download with retry (-c continues partial downloads, --tries=10 retries)
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org-shell_7.0.26_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org-server_7.0.26_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org-mongos_7.0.26_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-database-tools_100.13.0_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-mongosh_2.5.10_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org-database-tools-extra_7.0.26_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org-database_7.0.26_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org-tools_7.0.26_amd64.deb
wget -c --tries=10 https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/7.0/multiverse/binary-amd64/mongodb-org_7.0.26_amd64.deb

# Install all packages at once
sudo dpkg -i *.deb

# Fix any dependency issues
sudo apt install -f

# Wait 30-60 minutes and try again
sudo apt update
sudo apt install -y mongodb-org
```


## 5. configuration de 5GC
- utilise les deux chemins :
  1. ```cd open5gs/install/bin```
  2. ```cd open5gs/install/etc``` (**ici on trouve les fichiers de configuration**)

```bash
~/open5gs/install/etc/open5gs$ ls
amf.yaml   bsf.yaml  hss.yaml  nrf.yaml   pcf.yaml   scp.yaml    sepp2.yaml  sgwu.yaml  tls       udr.yaml
ausf.yaml  hnet      mme.yaml  nssf.yaml  pcrf.yaml  sepp1.yaml  sgwc.yaml   smf.yaml   udm.yaml  upf.yaml
user@user-VirtualBox:~/open5gs/install/etc/open5gs$ 
```

### parlons sur les fichiers de configuration : 
Les fichiers 5G dans la liste sont :
`amf.yaml, ausf.yaml, nrf.yaml, nssf.yaml, pcf.yaml, udm.yaml, udr.yaml, smf.yaml, upf.yaml, scp.yaml, sepp1.yaml, sepp2.yaml, bsf.yaml`.


| Fichier / Dossier           | Fonction réseau                                  | 4G/5G | Rôle principal                                                                       |
| --------------------------- | ------------------------------------------------ | ----- | ------------------------------------------------------------------------------------ |
| **amf.yaml**                | AMF – Access and Mobility Management Function    | 5G    | Gère la signalisation UE ↔ 5GC (authentification initiale, enregistrement, mobilité) |
| **ausf.yaml**               | AUSF – Authentication Server Function            | 5G    | Authentifie les abonnés 5G avec l’UDM                                                |
| **nrf.yaml**                | NRF – Network Repository Function                | 5G    | Découverte et enregistrement des fonctions réseau 5G                                 |
| **nssf.yaml**               | NSSF – Network Slice Selection Function          | 5G    | Sélectionne le slice approprié pour chaque UE                                        |
| **pcf.yaml**                | PCF – Policy Control Function                    | 5G    | Gestion des politiques (QoS, règles)                                                 |
| **udm.yaml**                | UDM – Unified Data Management                    | 5G    | Gestion des données des abonnés (remplace le HSS côté 5G)                            |
| **udr.yaml**                | UDR – Unified Data Repository                    | 5G    | Base de données pour UDM, PCF, etc.                                                  |
| **smf.yaml**                | SMF – Session Management Function                | 5G    | Gère les sessions PDU et attribue les adresses IP                                    |
| **upf.yaml**                | UPF – User Plane Function                        | 5G    | Plan utilisateur (transfert des paquets)                                             |
| **scp.yaml**                | SCP – Service Communication Proxy (optionnel 5G) | 5G    | Proxy entre fonctions réseau                                                         |
| **sepp1.yaml / sepp2.yaml** | SEPP – Security Edge Protection Proxy            | 5G    | Sécurise l’interconnexion entre PLMNs                                  
| **bsf.yaml** | **BSF – Binding Support Function** | Il stocke et fournit les informations de liaison (binding) entre les services et les abonnés. Il aide notamment le PCF et les fonctions réseau à retrouver rapidement où se trouve l’abonné ou sa session PDU. |

**il y a 13 fichiers (9 parmis eux essentiels pour nous -tous sauf scp sepp1 sepp2 bsf-)**

### configurer les fichiers, fait des modifications ,par exemple : commenter scp , et uncommenter nrf (dans les 13 fichiers) , verifier les addresses IP , verifier les parametres de mongodb (son lien..etc)

----------------------------------------
## 6. Aprés la configuration des fichiers , je lance les services 

```bash
#!/bin/bash
# ~/open5gs/install/run_5g.sh
# Lancer les services 5G Core Open5GS (sans SCP)

# Démarrer NRF (toujours en premier)
~/open5gs/install/bin/open5gs-nrfd -c ~/open5gs/install/etc/open5gs/nrf.yaml &

# Démarrer NSSF (après NRF, avant AMF)
~/open5gs/install/bin/open5gs-nssfd -c ~/open5gs/install/etc/open5gs/nssf.yaml &

# Démarrer AMF
~/open5gs/install/bin/open5gs-amfd -c ~/open5gs/install/etc/open5gs/amf.yaml &

# Démarrer AUSF
~/open5gs/install/bin/open5gs-ausfd -c ~/open5gs/install/etc/open5gs/ausf.yaml &

# Démarrer UDM
~/open5gs/install/bin/open5gs-udmd -c ~/open5gs/install/etc/open5gs/udm.yaml &

# Démarrer UDR
~/open5gs/install/bin/open5gs-udrd -c ~/open5gs/install/etc/open5gs/udr.yaml &

# Démarrer PCF
~/open5gs/install/bin/open5gs-pcfd -c ~/open5gs/install/etc/open5gs/pcf.yaml &

# Démarrer SMF
~/open5gs/install/bin/open5gs-smfd -c ~/open5gs/install/etc/open5gs/smf.yaml &

# Démarrer UPF
~/open5gs/install/bin/open5gs-upfd -c ~/open5gs/install/etc/open5gs/upf.yaml &
```

### some error ? (UPF is not working, because it needs sudo access) , in another terminal 
```bash
user@user-VirtualBox:~/open5gs/install$ sudo ~/open5gs/install/bin/open5gs-upfd -c ~/open5gs/install/etc/open5gs/upf.yaml 
```

As a result of (```ip a``` in a third terminal) , you must find a new interface **ogstun** existing but is **DOWN and has no IP address**, so the **UPF cannot pass** user traffic yet
 
# stop running les services
```bash
pkill -9 -f open5gs-
```


## pour passer vers dockerfile
n7ws 3la files .yaml wnbedel

path: /open5gs/install/var/log/open5gs/amf.log
instead of /home/user/open5gs/install/var/log/open5gs/amf.log
