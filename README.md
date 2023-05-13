[![MASTER](https://github.com/fourfridays/wagtail-batteries-included/actions/workflows/master.yaml/badge.svg?event=push)](https://github.com/fourfridays/wagtail-batteries-included/actions/workflows/master.yaml)

View demo website running at: https://wbi.fourfridays.com/

# Running locally

To run this repository locally please make sure to have docker and docker-compose installed on your computer.

### Steps:
1. Clone repo from master branch
2. Within the cloned folder in terminal run ` docker-compose run web python manage.py migrate `. This will apply all migrations to the database
3. Create SuperUser, ` docker-compose run web python manage.py createsuperuser `
4. Launch website locally, ` docker-compose up `. You can also run ` docker-compose up -d ` if you would like the service to run in the background
5. Login to the website by opening http://localhost:8080/admin in your browser of choice. Use the credentials you created in step 3 to login.

# Deploying on a Kubernetes (K8) cluster

Instructions assume you have a K8 cluser setup with Nginx Ingress, LetsEncrypt, and successfully running one or more nodes.

The container image tagged latest is the stable production ready image.

### Steps:
1. Create a new secrets file **outside** the repo titled prod-wbi-secrets for production node. The secret file should have the following environment variables.
```
# Please take care that you do not inadvertently commit any configuration secrets
DEFAULT_STORAGE_DSN=your_object_storage_dsn
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

2. Deploy secrets file in terminal from the location of where you saved the secrets file, ` kubectl create secret generic secret --from-env-file=prod-wbi-secrets `. After running the command you should receive a secret successfully created.

3. Edit values in the following yaml files under folder /kube/prod/
    - prod-configmap.yaml - change domain_aliases, csrf_trusted_origins to your domain
    - prod-deployment.yaml - nothing to change
    - prod-ingress.yaml - change annotations, and hosts to match your configuration

4. Deploy the app to your node by running the following from the root folder of the repo, ` kubectl apply -f ./kube/prod/ `. This should successfully deploy the app with one replica to your node. To check run ` kubectl get pods `.

5. Login to app runnning on the node, ` kubectl exec <your_pod_name> -it -- /bin/bash`
    - Run migration, ` python3 manage.py migrate `
    - Create superuser, ` python3 manage.py createsuperuser `
