# Overview:
I spent some time creating my own connect 4 game recently, and I focused heavily on creating a pretty UI and an AI bot with varying difficulty to play against. However, the purose of the **dev** and **main** branches of this repo were created for the purpose of exploring some basic DevOps tooling. So, I deployed a simple web version of my connect 4 game in order to solidify my understanding of CI/CD using Docker, Kubernetes, Helm, Github Actions, etc.

**if you are here for the UI/AI Connect 4 game, go to the 'experimental' branch.**

My goal was to understand how modern software projects are developled, deployed and maintained in a scalable, containerized enviornment.

# Dockerization:
A Dockerfile was created to package this app using a slim Python base image and a non-root user.

To build the Docker image locally:
```
docker build -t connect4-web .
```

To run the Docker container:
```
docker run -p 8000:8000 connect4-web
```
this allows for consistent enviornments across machines.

# Kubernetes with Minikube
I used minikube to simulate a kubernetes cluster on my local machine.

Deployed the app using kubectl:

```
kubectl create deployment connect4-web --image=connect4-web
kubectl expose deployment connect4-web --type=NodePort --port=8000
minikube service connect4-web --url
```

i also used commands like 
```
kubectl get pods
kubectl get svc
kubectl logs pod-name
```
this gave me an understanding of how deployments, services, and pods interact.

# Helm chart Integration

I created a helm chart (connect4-chart/) to template the kubernetes.
I created two values files: `values-dev.yaml` for dev: 1 replica, tag = latest, and `values-prod.yaml` for prod: 2 replicas, tag = commit SHA

I installed the chart with:
```
helm install connect4-dev ./connect4-chart -f values-dev.yaml --namespace dev
```

Using helm to make updates:
```
helm upgrade connect4-dev ...
```

# Environment Seperation:
I created seperate `dev` and `prod` kubernetes namespaces to isolate environments.
```
kubectl create namespace dev
```
```
kubectl create namespace prod
```
helm deployments target the correct namespace using:
```
--namespace dev --create-namespace
```

this makes sure I can test changes in `dev` without affecting production

# Branching strategy:

`dev` branch: used for development, all changes are tested here first
`main` branch: used for production deployments, only stable code is merged here.
`experimental` branchL used for UI/AI functionality, not connected to deployment.
When I want to promote changes, I merge dev into main.

# CI/CD with GitHub actions:

I configured github actions to automate the full pipeline:
When I push to `dev`, a Docker image is built and pushed to Docker hub, then deployed to `dev` namespace.
When I push to `main`, the same happens for `prod`.

each workflow uses a self-hosted runner so it cna access local minikube. they also each set docker tags to the commit SHA.
each workflow uses helm to deploy:
```
helm upgrade --install connect4-dev ...
```

Secrets:
`DOCKER_USERNAME`, `DOCKER_PASSWORD`, `KUBECONFIG_DATA` for accessing minikube from github actions

# Docker Hub integration

Created a public repository `connect4-web`
Docker image names follow this convention:
```
tevander232/connect4-web:<commit-sha>
```

# testing the setup:

to test a dev deployment:
1. make a change in the `dev` branch
2. commit and push 
3. watch the action run in github
4. confirm image shows up on docker hub
5. confirm pod updates with: `kubectl get pods -n dev`
6. open dev service: `minikube service connect4-dev-connect4-chart -n dev --url`

to promote to prod:
1. merge dev into main
2. push `main`, watch the prod action run
3. visit `minikube service connect4-prod-connect4-chart -n prod --url`

