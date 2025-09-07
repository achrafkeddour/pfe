Parfait 👍 je vais tout te répéter **depuis zéro jusqu’à avoir ton core 5G Open5GS qui tourne dans Docker**, bien organisé étape par étape :

---

## 🚀 Installation & Exécution complète d’Open5GS dans Docker

### 1️⃣ Récupérer le code source

```bash
git clone https://github.com/open5gs/open5gs
cd open5gs/docker
```

---

### 2️⃣ Construire les images Docker

```bash
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker

docker-compose build
```

---

### 3️⃣ Démarrer MongoDB + WebUI

```bash
docker-compose up -d mongodb webui
```

Vérifier :

```bash
docker ps
```

➡️ Tu dois voir `open5gs-mongodb` et `open5gs-webui` en **Up**.
Le WebUI est dispo ici 👉 [http://localhost:9999](http://localhost:9999)

---

### 4️⃣ Démarrer un conteneur pour compiler & lancer le Core

```bash
docker-compose run -d run
```

Vérifier :

```bash
docker ps
```

➡️ Tu dois voir ton container `docker_run_xxx` en **Up**.

---

### 5️⃣ Entrer dans ce conteneur

```bash
docker exec -it <ID_DU_CONTENEUR_RUN> /bin/bash
```

⚠️ remplace `<ID_DU_CONTENEUR_RUN>` par ce que tu as vu avec `docker ps`.

---

### 6️⃣ Compiler Open5GS dans le conteneur

```bash
cd /open5gs
meson build --prefix=`pwd`/install
# generally, here i got : Directory already configured.
ninja -C build
ninja -C build install
```

---

### 7️⃣ Vérifier que les binaires sont là

```bash
ls install/bin/
```

Tu dois voir des exécutables comme :

```
open5gs-amfd  open5gs-smfd  open5gs-upfd ...
```

---

### 8️⃣ Lancer le Core 5G (toutes les Network Functions)
- entrer dans les fichiers : amf.yaml , smf.yaml , upf.yaml , udm.yaml , ausf.yaml , pcf.yaml , nssf.yaml , bsf.yaml
- et **commenter les deux lignes de scp** ,puis **uncommenter les deux lignes de nrf**

- utiliser **db_uri: mongodb://mongodb/open5gs** (je sais pas est ce que vraiment mongodb remplace localhost ou non) au lieu de **db_uri: mongodb://localhost/open5gs** dans les fichiers suivantes :
  (may be zid dir **docker-compose restart run** - im not sure about it)
  
Toujours dans le conteneur :

```bash
./install/bin/open5gs-nrfd &
./install/bin/open5gs-amfd &
./install/bin/open5gs-smfd &
./install/bin/open5gs-upfd &
./install/bin/open5gs-ausfd &
./install/bin/open5gs-udmd &
./install/bin/open5gs-pcfd &
./install/bin/open5gs-nssfd &
./install/bin/open5gs-hssd &
```

---

### 9️⃣ Vérifier que tout tourne

```bash
ps -ef | grep open5gs
```

---

✅ À ce stade :

* MongoDB est OK
* WebUI fonctionne sur **localhost:9999**
* Tout le **Core 5G (Open5GS)** est lancé dans ton conteneur

---

* if i lost everything : i do **docker ps -a** , to see all dockers that i had before and restart them by : 
``` docker start container_name1 container_name2 ```

