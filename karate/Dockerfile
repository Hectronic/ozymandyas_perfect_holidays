# Dockerfile

# ——— Build & test stage ————————————————————————————————
FROM docker.io/library/openjdk:17-slim AS build

RUN apt-get update \
 && apt-get install -y maven \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN mvn clean test -B

