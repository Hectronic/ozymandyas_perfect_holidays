#!/usr/bin/env bash
#
# Build the Docker image and report success/failure of the build-and-test stage.

set -euo pipefail

IMAGE_NAME=karate-weather-tests

# build will run 'mvn clean test' as part of the Dockerfile
docker build -t ${IMAGE_NAME} .

# final container CMD is a no-op, so we just inspect the build exit code
echo "✅ Docker build (and tests) succeeded in image '${IMAGE_NAME}'"
