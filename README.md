# Microservices Kubernetes

Projet de programmation distribuée basé sur deux microservices déployés sur Minikube : `task-service` et `users-service`. Le projet utilise Flask, PostgreSQL et Kubernetes, avec une sécurisation RBAC sur le `task-service`.

## Description

Ce projet met en place une architecture microservices simple :
- `task-service` : gestion des tâches avec persistance PostgreSQL.
- `users-service` : gestion des utilisateurs.
- `Minikube` : exécution locale du cluster Kubernetes.
- `RBAC` : sécurisation d’accès pour le `task-service`.

L’objectif est de déployer, tester et sécuriser les services dans un cluster Kubernetes local. [web:469][web:402]

## Structure du projet

```text
Projet Prog Dist/
├── task-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init-db.sql
│   ├── ingress.yaml
│   ├── postgres-db.yaml
│   ├── rbac-task.yaml
│   ├── task-service-k8s.yaml
│   ├── task-service-v2-k8s.yaml
│   ├── task-service-v3-k8s.yaml
│   └── README.md
└── users-service/
    ├── app_users.py
    ├── Dockerfile
    ├── requirements.txt
    └── users-service-k8s.yaml
```

## Technologies utilisées

- Python / Flask
- PostgreSQL
- Docker
- Kubernetes
- Minikube
- Kubectl
- RBAC Kubernetes [web:402][web:466]

## Déploiement

### 1. Démarrer Minikube

```bash
minikube start
```

### 2. Déployer PostgreSQL et task-service

```bash
kubectl apply -f task-service/rbac-task.yaml
kubectl apply -f task-service/postgres-db.yaml
kubectl apply -f task-service/task-service-v3-k8s.yaml
```

### 3. Déployer users-service

```bash
kubectl apply -f users-service/users-service-k8s.yaml
```

### 4. Vérifier les ressources

```bash
kubectl get all
kubectl get sa
kubectl get role
kubectl get rolebinding
```

Les services Kubernetes permettent d’exposer les applications et de faciliter la communication réseau entre composants dans le cluster. [web:436][web:470]

## Tests API

### Task Service

Récupérer l’URL :
```bash
minikube service task-service --url
```

Lister les tâches :
```bash
curl $(minikube service task-service --url)/tasks
```

Créer une tâche :
```bash
curl -X POST $(minikube service task-service --url)/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"K8s","done":false}'
```

### Users Service

Récupérer l’URL :
```bash
minikube service users-service --url
```

Tester le service :
```bash
curl $(minikube service users-service --url)
```

## Sécurité

Le projet inclut une configuration RBAC pour le `task-service` avec :
- un `ServiceAccount`
- un `Role`
- un `RoleBinding`

Cela permet d’attribuer des permissions précises au service, conformément au modèle RBAC de Kubernetes. [web:402][web:422]

Vérification :
```bash
kubectl get sa task-service-sa
kubectl get role task-role
kubectl get rolebinding task-rolebinding
```

## État du projet

- `task-service` fonctionnel
- connexion PostgreSQL fonctionnelle
- table `tasks` créée et testée
- RBAC configuré sur `task-service`
- `users-service` présent dans l’architecture du projet

## Debug utile

```bash
kubectl logs deployment/task-service -f
kubectl describe deployment/task-service
kubectl exec deployment/postgres -- psql -U admin -d tasksdb -c "\dt"
```

## Auteur

Melina Kernou  
MLSD - Paris Cité  
Avril 2026
