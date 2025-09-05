# 📊 Présentation : Kubernetes – L’orchestrateur de conteneurs

---

## Diapositive 1 : Titre

**Kubernetes : Automatiser le déploiement et la gestion des conteneurs**

* Sous-titre : *De Docker à l’orchestration à grande échelle*

---

## Diapositive 2 : Qu’est-ce que Kubernetes ?

* Plateforme **open-source** développée par Google.
* Sert à **orchestrer** et gérer des conteneurs (souvent Docker).
* Automatise :

  * Déploiement
  * Mise à l’échelle (scaling)
  * Répartition de charge
  * Récupération après panne

🗣️ *Note orateur* : Imaginez une tour de contrôle qui gère des centaines d’avions (conteneurs) en toute sécurité.

---

## Diapositive 3 : Pourquoi Kubernetes ?

* Les applications modernes utilisent des **dizaines ou centaines de conteneurs**.
* Les gérer manuellement = trop complexe.
* Kubernetes apporte :

  * **Scalabilité automatique**
  * **Résilience** (auto-healing)
  * **Portabilité** (cloud, on-premise, hybride)

---

## Diapositive 4 : Architecture Kubernetes

* **Cluster** = ensemble de machines (nodes).
* **Master Node (Control Plane)** :

  * API Server
  * Scheduler
  * Controller Manager
  * etcd (base clé-valeur pour la config)
* **Worker Nodes** :

  * Kubelet (agent)
  * Kube-proxy (réseau)
  * Pods (unités d’exécution)

---

## Diapositive 5 : Concepts Clés

* **Pod** : plus petite unité → encapsule un ou plusieurs conteneurs.
* **Deployment** : définit le nombre de pods, la mise à jour, le rollback.
* **Service** : expose les pods via un IP ou load balancer.
* **ConfigMap & Secret** : gestion de la configuration et des infos sensibles.
* **Namespace** : isolation logique dans un cluster.

---

## Diapositive 6 : Exemple simple – Déploiement Nginx

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

Commande pour appliquer :

```bash
kubectl apply -f nginx-deploy.yaml
```

---

## Diapositive 7 : Services Kubernetes

* **ClusterIP** : accessible uniquement dans le cluster.
* **NodePort** : accessible depuis l’extérieur via un port fixe.
* **LoadBalancer** : crée un load balancer externe (cloud).
* **Ingress** : gestion avancée du routage HTTP/HTTPS.

---

## Diapositive 8 : Avantages de Kubernetes

* 🚀 Mise à l’échelle automatique
* 🔁 Auto-réparation (redémarre les pods défaillants)
* 🌍 Portabilité (multi-cloud, bare metal, cloud hybride)
* 🛡️ Gestion simplifiée de la sécurité et configuration
* 🔗 Intégration native avec monitoring, CI/CD, service mesh

---

## Diapositive 9 : Écosystème Kubernetes

* **Kubectl** → CLI de gestion.
* **Helm** → gestionnaire de packages (charts).
* **Operators** → automatisation avancée.
* **Prometheus & Grafana** → monitoring.
* **Istio / Linkerd** → service mesh.

---

## Diapositive 10 : Cas d’utilisation

* Héberger des **microservices**.
* Applications **cloud-native**.
* Big Data et IA (Spark, ML pipelines).
* 5G & Telco (comme **Open5GS** avec réseau 4G/5G virtualisé).
* Plateformes SaaS multi-tenant.

---

## Diapositive 11 : Bonnes Pratiques

* Définir des **ressources (CPU, mémoire)** par pod.
* Utiliser des **namespaces** pour organiser.
* Séparer **ConfigMaps/Secrets** du code.
* Mettre en place des sondes (**liveness/readiness probes**).
* Automatiser via CI/CD et Helm.

---

## Diapositive 12 : Kubernetes & Docker

* Docker crée et exécute des conteneurs.
* Kubernetes orchestre **des centaines/milliers** de conteneurs.
  👉 Docker = outil de base
  👉 Kubernetes = gestion à grande échelle

---

## Diapositive 13 : Conclusion

* Kubernetes est la **colonne vertébrale des applications cloud-native**.
* Apporte **scalabilité, fiabilité et automatisation**.
* Étape incontournable après Docker pour les **microservices et les télécoms (Open5GS)**.

💡 *Citation* : *« Kubernetes n’exécute pas seulement vos conteneurs, il exécute vos idées à l’échelle. »*

