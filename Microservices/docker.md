# 📊 Présentation : Docker – Conteneurisation Simplifiée

---

## Diapositive 1 : Titre

**Docker : L’outil de conteneurisation moderne**

* Sous-titre : *Construire, expédier et exécuter vos applications partout*

---

## Diapositive 2 : Qu’est-ce que Docker ?

* Plateforme open-source pour **développer, expédier et exécuter** des applications dans des **conteneurs**.
* Conteneur = unité légère et portable qui contient :

  * Le code
  * Les bibliothèques
  * Les dépendances
* Fonctionne de la même manière sur n’importe quel environnement.

🗣️ *Note orateur* : Imaginez une boîte où vous emballez tout ce dont votre appli a besoin → vous pouvez la transporter et l’exécuter partout.

---

## Diapositive 3 : Conteneurs vs. Machines Virtuelles (VMs)

**VMs (Machines Virtuelles)**

* Incluent un OS complet.
* Lourdes et lentes à démarrer.
* Consomment beaucoup de ressources.

**Conteneurs (Docker)**

* Partagent le noyau de l’OS hôte.
* Légers et démarrent en quelques secondes.
* Idéals pour la **scalabilité et la portabilité**.

---

## Diapositive 4 : Architecture Docker

* **Docker Client** : interface en ligne de commande (docker CLI).
* **Docker Daemon** : exécute et gère les conteneurs.
* **Docker Images** : modèles immuables pour créer des conteneurs.
* **Docker Hub / Registry** : dépôt d’images (comme GitHub pour le code).

---

## Diapositive 5 : Concepts Clés

* **Image** : une "recette" (blueprint) de votre application.
* **Conteneur** : instance en cours d’exécution d’une image.
* **Dockerfile** : fichier décrivant comment construire une image.
* **Volume** : stockage persistant.
* **Network** : communication entre conteneurs.

---

## Diapositive 6 : Avantages de Docker

* 🚀 Rapidité et légèreté
* 🛠️ Cohérence entre environnements (dev, test, prod)
* 📦 Isolation des applications
* 🔄 CI/CD simplifié
* 🌍 Écosystème riche (Docker Hub, Compose, Swarm, Kubernetes)

---

## Diapositive 7 : Exemple simple

Un fichier **Dockerfile** minimal pour une app Node.js :

```dockerfile
FROM node:18  
WORKDIR /app  
COPY . .  
RUN npm install  
CMD ["node", "server.js"]  
```

* Construire l’image : `docker build -t myapp .`
* Lancer un conteneur : `docker run -p 3000:3000 myapp`

---

## Diapositive 8 : Docker Compose

* Permet de définir et gérer **plusieurs conteneurs** via un fichier `docker-compose.yml`.
* Exemple : une app + une base de données :

```yaml
version: "3"
services:
  web:
    build: .
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
```

Lancer avec : `docker-compose up`

---

## Diapositive 9 : Cas d’utilisation de Docker

* Développement rapide et reproductible.
* Tests d’intégration et CI/CD.
* Microservices et architecture cloud-native.
* Déploiement dans le cloud (AWS, GCP, Azure).
* Virtualisation légère dans les télécoms (comme Open5GS).

---

## Diapositive 10 : Bonnes Pratiques

* Écrire des **Dockerfiles optimisés** (multi-stage builds, images légères).
* Utiliser des **volumes** pour la persistance.
* Scanner les images pour la **sécurité**.
* Gérer les logs et la supervision.
* Automatiser avec CI/CD et Kubernetes.

---

## Diapositive 11 : Docker vs Kubernetes

* **Docker** = construit et exécute des conteneurs.
* **Kubernetes** = orchestre des centaines/milliers de conteneurs.
  👉 Docker est le **point de départ**, Kubernetes est l’**étape suivante**.

---

## Diapositive 12 : Conclusion

* Docker = **léger, portable et puissant**.
* Simplifie le développement, le test et le déploiement.
* Étape essentielle pour aller vers les **microservices et le cloud-native**.

💡 *Citation* : *« Emballez une fois, exécutez partout. »*

