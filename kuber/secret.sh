kubectl create configmap nl2ml-form-config --from-file=config/config.py
kubectl create configmap nl2ml-form-db-initscript --from-file=../db/init.sql
kubectl create secret generic regcred-nl2ml --from-file=.dockerconfigjson=./config/deploy-token.json \
    --type=kubernetes.io/dockerconfigjson
