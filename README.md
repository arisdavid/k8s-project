# Kubernetes Demo Project (Python Producer, Consumer and Kafka)

## Introduction
This is mini-project demonstrating how to deploy and run a kafka server and python applications inside a Kubernetes cluster. 
Producer.py publishes a message into a kafka topic while consumer.py listens and prints these messages. 

Optional: for interacting with the cluster it would be handy to have k9s installed - https://github.com/derailed/k9s. It's an interactive UI tool for interacting with Kubernetes cluster. 

## Local Development

For local development and testing setup a Kubernetes cluster using minikube. 
The minikube cluster is where the python apps, redis and kafka server will be deployed.

https://kubernetes.io/docs/setup/learning-environment/minikube/ 

Launch a minikube cluster using the following command:

``` minikube start ```

Create a namespace within the cluster called k8demo

``` minikube create namespace k8demo ```

Ensure you're inside the Kubernetes environment as this is where the images will be built
``` eval $(minikube docker-env) ```

## Install Helm
Helm is a tool for managing Kubernetes charts. Charts are packages of pre-configured Kubernetes resources.
To install Helm, refer to the Helm install guide and ensure that the helm binary is in the PATH of your shell.

## Add Repo
Add bitnami charts into the repo

``` 
helm repo add bitnami https://charts.bitnami.com/bitnami 
```

## Deploy kafka

```
helm install k8-kafka bitnami/kafka --namespace=k8demo \
--set persistence.enabled=false --set zookeeper.persistence.enabled=false
```

### Build the producer-app docker image (inside minikube cluster)
 
```
docker build -t producer-app:latest -f ./producer/Dockerfile producer
```

### Build the consumer-app docker image (inside minikube cluster)

```
docker build -t consumer-app:latest -f ./consumer/Dockerfile consumer
```

### Publish a message into a kafka topic
``` 
kubectl run producer --rm --tty -i --env="KAFKA_HOST=k8-kafka.k8demo.svc.cluster.local:9092" \
--image producer-app:latest --image-pull-policy Never --restart Never \
--namespace k8demo --command -- python -u /producer_app.py <message> <topic>
 ```
### Read messages from a specific topic
```
kubectl run consumer --rm --tty -i --env="KAFKA_HOST=k8-kafka.k8demo.svc.cluster.local:9092" \ 
--image consumer-app:latest --image-pull-policy Never --restart Never \ 
--namespace k8demo --command -- python -u /consumer_app.py <topic>
```

### Screenshots
![Image of K9s](https://github.com/arisdavid/k8s-project/blob/master/demo/k9s.png)




