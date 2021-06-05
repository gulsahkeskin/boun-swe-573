# syntax=docker/dockerfile:1

# Dockerfile is a standardized way for Docker to build Docker Image.

# We need to say to Docker what base image we would like to use for our application.
FROM python:3

# The environment variable ensures that the the python output is
# set straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# Create root directory for the project in the container
RUN mkdir /MediTagProject

# Set working directory to /MediTagProject
WORKDIR /MediTagProject

# Copy the contents of current directory into the container
ADD . /MediTagProject/

# Install any needed packages placed in requirements.txt
RUN pip install -r requirements.txt