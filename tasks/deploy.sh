#!/bin/bash

PROJECT="schneider-poc-cli-final"

if [ -z $1 ] || [ -z $2 ] ; then
	echo "Usage: $0 <dev|production|acceptance> <version>"
	exit 1
fi

echo "Starting deploy script ..."

ENV=${1%/}

if [ $ENV = "dev" ] || [ $ENV = "acceptance" ] || [ $ENV = "production" ]
then
    echo Deploying on $ENV

    if [ -d "build" ]
    then
        rm -rf build
    fi
    mkdir build

    cp appengine_config.py build/appengine_config.py
    cp -r src build/
    cp -r config build/

    if [ $ENV != "dev" ]
    then
        cp -r deployments/$ENV/config.py build/config/config.py
    fi

    cp -r lib/ build/lib
    cp app.yaml build/app.yaml
    cp main.py build/main.py
    cd build

    if [ $ENV != "production" ]
    then
      sed -i -e "s/service: default/service: default-$ENV/g" app.yaml
    fi

    sanitized_version=$(echo $2 | tr . -)
    echo $sanitized_version
    gcloud app deploy app.yaml --version=${sanitized_version} --project=$PROJECT --no-promote

else
    echo "Wrong environment. (dev | production | acceptance)."
fi