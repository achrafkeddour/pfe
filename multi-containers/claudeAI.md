Excellente question ! Pour passer **directement** à l'architecture multi-conteneurs sur une nouvelle VM (VM2) sans passer par l'étape du conteneur unique, voici les étapes complètes :

## 🚀 **Installation directe Multi-Conteneurs sur VM2**

### **Étapes après l'installation de Docker :**

```bash
# 1️⃣ Récupérer le code source
git clone https://github.com/open5gs/open5gs
cd open5gs

# 2️⃣ Installer Docker et Docker Compose
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker
```

### **3️⃣ Créer la structure de projet**
```bash
# Créer un répertoire dédié pour l'architecture multi-conteneurs
mkdir ~/open5gs-multicontainer
cd ~/open5gs-multicontainer

# Copier le dossier webui depuis le repo cloné
cp -r ~/open5gs/webui ./
```

### **4️⃣ Créer tous les fichiers nécessaires**

Créez ces 4 fichiers dans `~/open5gs-multicontainer/` :

1. **`docker-compose.yml`** (utilisez le fichier de l'artifact 1 que j'ai créé)
2. **`Dockerfile.ubuntu`** (utilisez le fichier de l'artifact 2)
3. **`setup_configs.sh`** (utilisez le fichier de l'artifact 3)
4. **`deploy.sh`** (utilisez le fichier de l'artifact 4)

### **5️⃣ Script d'installation complète pour VM2**

```bash
#!/bin/bash

echo "================================================"
echo "🚀 Installation directe Open5GS Multi-Conteneurs"
echo "================================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -d "~/open5gs-multicontainer" ]; then
    echo "❌ Erreur: Assurez-vous d'être dans ~/open5gs-multicontainer"
    exit 1
fi

# Étape 1: Créer le Dockerfile pour WebUI
echo "📦 Création du Dockerfile pour WebUI..."
cat > webui/Dockerfile << 'EOF'
FROM node:14-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

ENV NODE_ENV=production
ENV DB_URI=mongodb://mongodb:27017/open5gs
ENV HOSTNAME=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "run", "dev"]
EOF

# Étape 2: Rendre les scripts exécutables
echo "🔧 Configuration des permissions..."
chmod +x setup_configs.sh deploy.sh

# Étape 3: Créer les configurations
echo "📝 Génération des fichiers de configuration..."
./setup_configs.sh

# Étape 4: Construire toutes les images
echo "🏗️ Construction des images Docker..."
echo "   Cela peut prendre 10-15 minutes la première fois..."

# Construire l'image de base Open5GS
docker build -f Dockerfile.ubuntu -t open5gs-base .

# Construire WebUI
cd webui && docker build -t open5gs-webui . && cd ..

# Étape 5: Créer le réseau Docker
echo "🌐 Création du réseau Docker..."
docker network create --subnet=10.45.0.0/16 open5gs_net 2>/dev/null || true

# Étape 6: Démarrer MongoDB d'abord
echo "💾 Démarrage de MongoDB..."
docker-compose up -d mongodb

# Attendre que MongoDB soit prêt
echo "⏳ Attente de MongoDB (15 secondes)..."
sleep 15

# Vérifier que MongoDB est OK
if ! docker exec open5gs-mongodb mongo --eval "db.adminCommand('ping')" &>/dev/null; then
    echo "❌ MongoDB n'est pas prêt. Vérifiez avec: docker logs open5gs-mongodb"
    exit 1
fi

echo "✅ MongoDB est prêt!"

# Étape 7: Démarrer WebUI
echo "🌐 Démarrage de WebUI..."
docker-compose up -d webui
sleep 5

# Étape 8: Démarrer NRF (Network Repository Function)
echo "📡 Démarrage du NRF (registre central)..."
docker-compose up -d nrf
sleep 10

# Étape 9: Démarrer les fonctions de base de données
echo "💿 Démarrage des fonctions avec base de données..."
docker-compose up -d udr pcf bsf hss
sleep 5

# Étape 10: Démarrer les autres fonctions de contrôle
echo "🎛️ Démarrage des fonctions de contrôle..."
docker-compose up -d ausf udm nssf
sleep 5

# Étape 11: Démarrer AMF et SMF
echo "📶 Démarrage d'AMF et SMF..."
docker-compose up -d amf smf
sleep 5

# Étape 12: Démarrer UPF (User Plane)
echo "🚦 Démarrage d'UPF (User Plane)..."
docker-compose up -d upf

# Étape 13: Vérification finale
echo ""
echo "================================================"
echo "✅ Installation terminée!"
echo "================================================"
echo ""

# Afficher le statut
docker-compose ps

echo ""
echo "📊 Résumé de l'installation:"
echo "   - MongoDB: ✅ Port 27017"
echo "   - WebUI:   ✅ http://localhost:9999"
echo "   - NRF:     ✅ 10.45.0.10:7777"
echo "   - AMF:     ✅ 10.45.0.11 (NGAP: 38412/sctp)"
echo "   - SMF:     ✅ 10.45.0.12"
echo "   - UPF:     ✅ 10.45.0.13"
echo "   - AUSF:    ✅ 10.45.0.14"
echo "   - UDM:     ✅ 10.45.0.15"
echo "   - UDR:     ✅ 10.45.0.16"
echo "   - PCF:     ✅ 10.45.0.17"
echo "   - NSSF:    ✅ 10.45.0.18"
echo "   - BSF:     ✅ 10.45.0.19"
echo "   - HSS:     ✅ 10.45.0.20"
echo ""
echo "🔍 Commandes utiles:"
echo "   docker-compose logs -f <service>  # Voir les logs"
echo "   docker-compose restart <service>  # Redémarrer un service"
echo "   docker-compose ps                 # Voir l'état"
echo "   docker-compose down               # Tout arrêter"
echo ""
echo "📱 Prochaine étape:"
echo "   Configurez vos abonnés dans http://localhost:9999"
echo "   Login: admin / Password: 1423"
```

### **6️⃣ Commande complète pour VM2**

Voici un script tout-en-un pour configurer VM2 depuis zéro :## 📋 **Résumé des étapes pour VM2 :**

### **Installation rapide (commandes à exécuter) :**

```bash
# 1. Installer Docker
sudo apt update
sudo apt install -y docker.io docker-compose git
sudo usermod -aG docker $USER
newgrp docker

# 2. Cloner Open5GS (juste pour récupérer webui)
cd ~
git clone https://github.com/open5gs/open5gs

# 3. Créer le projet multi-conteneurs
mkdir ~/open5gs-multicontainer
cd ~/open5gs-multicontainer
cp -r ~/open5gs/webui ./

# 4. Créer les 4 fichiers que j'ai fournis
# - docker-compose.yml
# - Dockerfile.ubuntu
# - setup_configs.sh
# - deploy.sh
# - install_direct.sh (le nouveau script)

# 5. Rendre exécutables et lancer
chmod +x *.sh
./install_direct.sh
```

## ✅ **Avantages de cette approche :**

1. **Pas de passage par le conteneur unique** - directement multi-conteneurs
2. **Installation plus rapide** - pas de double compilation
3. **Architecture propre dès le départ**
4. **Chaque composant isolé** dès le début

## 🔍 **Vérification après installation :**

```bash
# Voir tous les conteneurs
docker ps

# Vérifier les logs
docker-compose logs -f nrf  # ou amf, smf, etc.

# Tester la connectivité
docker exec open5gs-amf ping 10.45.0.10
```

## 📝 **Note importante :**

Sur VM2, vous n'avez **PAS BESOIN** de :
- Compiler manuellement Open5GS
- Modifier les fichiers YAML un par un
- Lancer les binaires avec `&`

Tout est automatisé dans les Dockerfiles et docker-compose !

Cette approche est beaucoup plus propre et professionnelle pour un déploiement en production. Chaque Network Function a son propre conteneur avec sa propre configuration.
