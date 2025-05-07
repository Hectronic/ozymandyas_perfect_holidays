#!/bin/bash
set -e

# Nombre de la imagen
IMAGE_NAME=weather-tests

# Construye la imagen Docker
docker build -t $IMAGE_NAME .

# Ejecuta un contenedor y borra tras la ejecución
docker run --rm $IMAGE_NAME
