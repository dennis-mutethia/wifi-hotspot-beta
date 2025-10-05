# Use python base image
FROM python:3.13-slim-bullseye

# Update packages, install git, and clean up
RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#copy requirements.txt to working directory
COPY requirements.txt .

#update pip & install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
    