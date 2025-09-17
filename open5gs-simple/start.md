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
| **sepp1.yaml / sepp2.yaml** | SEPP – Security Edge Protection Proxy            | 5G    | Sécurise l’interconnexion entre PLMNs                                                |

| Fichier      | Fonction réseau                    | Rôle                                                                                                                                                                                                           |
| ------------ | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bsf.yaml** | **BSF – Binding Support Function** | Il stocke et fournit les informations de liaison (binding) entre les services et les abonnés. Il aide notamment le PCF et les fonctions réseau à retrouver rapidement où se trouve l’abonné ou sa session PDU. |


