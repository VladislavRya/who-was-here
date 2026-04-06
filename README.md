# Кто недавно был здесь (who was here)

Веб-приложение на python Flask + Redis, развёртываемое в двух Docker-контейнерах с помощью minikube.

Позволяет отметиться (ввести своё имя) и посмотреть, кто заходил за последний час.

## Требования

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Docker](https://docs.docker.com/get-docker/)

## Запуск

```bash
minikube start
eval $(minikube docker-env)
docker build -t who-was-here:latest ./app
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl get pods -w
sg docker -c "kubectl port-forward service/who-was-here 5000:5000 --address 0.0.0.0" 2>&1
```

## Остановка

```bash
kubectl delete -f k8s/app-deployment.yaml
kubectl delete -f k8s/redis-deployment.yaml
minikube stop
```
