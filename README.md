# monitoring
## Description
Ce projet permet de surveiller les métriques de sécurité des dépendances de différents services en utilisant Snyk, Prometheus et Grafana. Les métriques sont extraites des logs Snyk et exposées via un endpoint Prometheus pour être visualisées dans Grafana.

## Structure du projet
```
.
├── dashboard/
│   ├── grafana.json
├── docker-compose.yaml
├── grafana/
│   ├── datasources.yml
├── logs/
│   ├── snyk-categories.log
│   ├── snyk-cities.log
│   ├── snyk-communities.log
│   ├── snyk-products.log
├── prometheus/
│   ├── prometheus.yml
├── queries/
│   ├── queries.promql
├── snyk/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── snyk.py


```

## Prérequis
- Docker
- Docker Compose

## Installation
1. Clonez le dépôt :
    ```sh
    git clone https://github.com/tTwoAtos/monitoring
    cd foodstock_monitoring
    ```


2. Construisez et démarrez les conteneurs :
    ```sh
    docker-compose up --build -d
    ```

## Utilisation
- Accédez à Grafana à l'adresse `http://localhost:3000` avec les identifiants par défaut :
    - Utilisateur : `admin`
    - Mot de passe : grafana
- Les métriques Snyk sont exposées à l'endpoint `http://localhost:9469/metrics`.

## Configuration
- Les fichiers de configuration pour Prometheus est dans le répertoire prometheus avec prometheus.yaml
- Les dashboards Grafana sont définis dans grafana.json