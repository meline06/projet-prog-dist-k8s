# 🚀 Task Service Kubernetes 

Application **Flask CRUD Tasks** avec **PostgreSQL** déployée sur **Minikube** + **RBAC sécurité**.

## 🎯 Fonctionnalités
- ✅ **CRUD complet** : GET/POST tasks
- ✅ **PostgreSQL** : tasksdb + table `tasks(id,title,description,done)`
- ✅ **Service LoadBalancer** : `minikube service task-service`
- ✅ **RBAC sécurité** : ServiceAccount + Role + RoleBinding

## 🔧 Déploiement (5min)

### 1. Images Docker
```bash
docker build -t melinee/task-service:v4 .
docker push melinee/task-service:v4
```

### 2. Kubernetes
```bash
minikube start
kubectl apply -f rbac-task.yaml postgres-v3-k8s.yaml task-service-v3-k8s.yaml
kubectl rollout status deployment/task-service
```

### 3. Accès
```bash
minikube service task-service --url
curl $(minikube service task-service --url)/tasks
```

## 📋 API REST
GET /tasks → [{"id":1,"title":"Kubernetes OK","done":false}]
POST /tasks → {"id":2,"title":"Minikube","done":false}


**Test POST** :
```bash
curl -X POST $(minikube service task-service --url)/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"K8s","done":false}'
```

## 🛡️ Sécurité RBAC 
ServiceAccount: task-service-sa ✓
Role: task-role (pods/services get,list) ✓
RoleBinding: task-rolebinding ✓

```bash
kubectl get sa task-service-sa
kubectl get role task-role  
kubectl get rolebinding task-rolebinding
```

**Vulnérabilités** : Docker Hub Security Scan activé

## 📊 Status actuel
$(minikube service task-service --url)/tasks → ✅ 2 tasks
RBAC → kubectl get sa,role,rolebinding | grep task → ✅ actif
Postgres → kubectl exec deployment/postgres -- psql -U admin -d tasksdb -c "\dt" → ✅ table tasks

## 🏗️ Architecture
Minikube → Deployment(task-service:v4) → Service(LoadBalancer)
↓
PostgreSQL(tasksdb) ← RBAC


## 🔍 Debug & Monitoring
```bash
kubectl logs deployment/task-service -f
kubectl exec deployment/postgres -- psql -U admin -d tasksdb -c "\dt"
kubectl describe deployment task-service
```

## 📁 Fichiers
├── app.py # Flask CRUD
├── Dockerfile # Python slim
├── rbac-task.yaml # Sécurité RBAC
├── postgres-v3-k8s.yaml # PostgreSQL StatefulSet
├── task-service-v3-k8s.yaml # Deployment + Service
└── README.md # Ce fichier

**Microservices** : 
- task-service (ce dossier) : CRUD tasks + RBAC
- ../users-service/ : Users management

## 🎓 Notes 
- **Réseau** : Service discovery postgres → TCP 5432 OK
- **Sécurité** : RBAC + Docker Hub scan  
- **Observabilité** : Logs + psql + describe
- **Production** : Schema strict + ServiceAccount

**Auteur** : Melina kernou (MLSD Paris Cité)
**Date** : Avril 2026
