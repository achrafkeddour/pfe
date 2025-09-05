# 📊 Présentation : Cloud-Native – Construire pour l’avenir

---

## Diapositive 1 : Titre

**Cloud-Native : L’approche moderne des applications**

* Sous-titre : *Évolutivité, résilience et agilité par conception*

---

## Diapositive 2 : Qu’est-ce que le Cloud-Native ?

* Une **philosophie** et un **ensemble de pratiques** pour développer des applications adaptées au cloud.
* Applications **conçues pour être déployées, scalées et résilientes** dans des environnements distribués.
* Pas seulement une technologie → un **mode de pensée**.

🗣️ *Note orateur* : Cloud-native = penser « nuage » dès la conception, pas juste déplacer une appli existante dans le cloud.

---

## Diapositive 3 : Principes Cloud-Native

* **Microservices** : architecture modulaire.
* **Conteneurs** : portabilité (Docker).
* **Orchestration** : gestion massive (Kubernetes).
* **Automatisation CI/CD** : livraisons rapides et fiables.
* **Observabilité** : logs, métriques et traces centralisés.

---

## Diapositive 4 : CNCF (Cloud Native Computing Foundation)

* Fondation open-source créée en 2015 (sous Linux Foundation).
* Héberge des projets phares :

  * **Kubernetes**
  * **Prometheus** (monitoring)
  * **Envoy** (proxy)
  * **Helm** (packages)
  * **Jaeger** (tracing)
* Objectif : construire un **écosystème interopérable et ouvert**.

---

## Diapositive 5 : Les 12-Factor Apps (Bonnes pratiques Cloud-Native)

1. **Codebase unique**
2. **Dépendances explicites**
3. **Configuration externe**
4. **Services de backing** (BD, cache)
5. **Build, release, run séparés**
6. **Stateless processes**
7. **Port binding**
8. **Concurrence par scaling**
9. **Disposabilité rapide**
10. **Parité dev/prod**
11. **Logs comme flux d’événements**
12. **Admin processes séparés**

---

## Diapositive 6 : Avantages Cloud-Native

* 🚀 **Agilité** : livrer plus vite.
* 📈 **Scalabilité élastique**.
* 🔒 **Résilience** (auto-réparation, tolérance aux pannes).
* 🌍 **Portabilité multi-cloud**.
* 🛠️ **Innovation rapide** grâce à l’open-source CNCF.

---

## Diapositive 7 : Défis Cloud-Native

* Complexité accrue (infrastructure + outils).
* Besoin de **compétences DevOps** solides.
* Sécurité distribuée.
* Gestion des coûts cloud.
* Observabilité indispensable.

---

## Diapositive 8 : Stack Cloud-Native typique

* **Code** : Microservices (Node.js, Go, Java, Python, Rust…)
* **Conteneurs** : Docker, Podman
* **Orchestration** : Kubernetes
* **CI/CD** : GitLab CI, Jenkins, ArgoCD
* **Monitoring** : Prometheus, Grafana
* **Tracing** : Jaeger, OpenTelemetry
* **Service Mesh** : Istio, Linkerd
* **Cloud** : AWS, GCP, Azure, ou on-prem

---

## Diapositive 9 : Cas d’utilisation

* Applications SaaS modernes.
* Plateformes 5G / Telco (comme **Open5GS**) → chaque fonction réseau en microservice.
* Applications Big Data et IA distribuées.
* Solutions multi-tenant.
* Entreprises cherchant **scalabilité + rapidité d’innovation**.

---

## Diapositive 10 : Exemple Cloud-Native – Open5GS

* Composants (MME, HSS, AMF, UPF, etc.) packagés en conteneurs.
* Déployés sur Kubernetes.
* Supervision via Prometheus/Grafana.
* CI/CD pour tester rapidement les releases.
* Résilience → si un composant tombe, Kubernetes le redémarre.

---

## Diapositive 11 : Bonnes pratiques Cloud-Native

* Adopter **CI/CD** dès le début.
* Mettre en place **observabilité** (logs, métriques, traces).
* Définir des **limites de ressources** pour les pods.
* Gérer la **sécurité par design** (RBAC, secrets).
* Privilégier les services managés (DBaaS, monitoring cloud).

---

## Diapositive 12 : Conclusion

* Cloud-Native = **plus qu’une technologie : une philosophie**.
* Repose sur : **Microservices + Conteneurs + Kubernetes + CI/CD + Observabilité**.
* Idéal pour des projets comme **Open5GS**, qui nécessitent **agilité, scalabilité et résilience**.

💡 *Citation* : *« Cloud-Native, c’est construire pour l’échec, mais penser à l’échelle. »*

