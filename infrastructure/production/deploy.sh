#!/bin/bash

set -e

# Check for environment variables
checkEnvVariableExists() {
    if [ -z ${!1} ]
    then
        echo "ERROR: Define $1 environment variable."
        exit 1
    else
        echo "INFO: $1 environment variable found."
    fi
}
checkEnvVariableExists CODEWOF_IMAGE_TAG
checkEnvVariableExists CODEWOF_DOMAIN

# Update Django service
docker service update --image ghcr.io/uccser/codewof:${CODEWOF_IMAGE_TAG} codewof_django

# Run updata_data command
if docker service ps codewof_update-data | grep codewof_update-data
then
    docker service update --image ghcr.io/uccser/codewof:${CODEWOF_IMAGE_TAG} codewof_update-data
else
    docker service create \
    --name codewof_update-data \
    --detach \
    --mode replicated-job \
    --label traefik.enable=false \
    --network codewof_backend \
    --constraint node.role==worker \
    --constraint node.labels.role==apps \
    --env POSTGRES_HOST="postgres" \
    --env=POSTGRES_PORT="5432" \
    --env=DEPLOYMENT_ENVIRONMENT_FILE="/codewof_deployment_environment" \
    --env=DJANGO_SECRET_KEY_FILE="/run/secrets/codewof_django_secret_key" \
    --env=POSTGRES_DB_FILE="/run/secrets/codewof_postgres_db" \
    --env=POSTGRES_USER_FILE="/run/secrets/codewof_postgres_user" \
    --env=POSTGRES_PASSWORD_FILE="/run/secrets/codewof_postgres_password" \
    --config codewof_deployment_environment \
    --secret codewof_django_secret_key \
    --secret codewof_postgres_db \
    --secret codewof_postgres_user \
    --secret codewof_postgres_password \
    --restart-condition none \
    ghcr.io/uccser/codewof:${CODEWOF_IMAGE_TAG} python ./manage.py sampledata
fi

# TODO: Setup cron job for backdate task (tasks/backdate/)