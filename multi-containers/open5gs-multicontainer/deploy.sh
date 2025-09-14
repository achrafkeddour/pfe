#!/bin/bash

echo "🚀 Déploiement d'Open5GS en architecture multi-conteneurs"

# Arrêter les conteneurs existants
echo "1. Arrêt des conteneurs existants..."
docker-compose down

# Créer les fichiers de configuration
echo "2. Création des fichiers de configuration..."
chmod +x setup_configs.sh
./setup_configs.sh

# Construire les images
echo "3. Construction des images Docker..."
docker-compose build

# Démarrer MongoDB et WebUI
echo "4. Démarrage de MongoDB et WebUI..."
docker-compose up -d mongodb webui

# Attendre que MongoDB soit prêt
echo "5. Attente de MongoDB..."
sleep 10

# Démarrer NRF en premier (c'est le registre central)
echo "6. Démarrage du NRF..."
docker-compose up -d nrf
sleep 5

# Démarrer les autres composants du control plane
echo "7. Démarrage des fonctions du Control Plane..."
docker-compose up -d ausf udm udr pcf nssf bsf
sleep 5

# Démarrer AMF et SMF
echo "8. Démarrage d'AMF et SMF..."
docker-compose up -d amf smf
sleep 5

# Démarrer UPF (User Plane)
echo "9. Démarrage d'UPF..."
docker-compose up -d upf

# Démarrer HSS pour la compatibilité 4G
echo "10. Démarrage d'HSS..."
docker-compose up -d hss

echo ""
echo "✅ Déploiement terminé !"
echo ""
echo "📊 Vérification des conteneurs:"
docker-compose ps

echo ""
echo "🌐 Accès:"
echo "   - WebUI: http://localhost:9999"
echo "   - MongoDB: localhost:27017"
echo ""
echo "🔍 Commandes utiles:"
echo "   - Voir les logs d'un composant: docker-compose logs -f <service>"
echo "   - Redémarrer un service: docker-compose restart <service>"
echo "   - Arrêter tout: docker-compose down"
echo "   - Voir l'état: docker-compose ps"
