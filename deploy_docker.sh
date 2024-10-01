#!/bin/bash

cd html
./clean.sh
cd ..

# Step 1: Build the Docker image
sudo docker build -t pg50226-drumlace .

# Step 2: Run the Docker container (optional)
# Uncomment the next line if you want to run the container for testing
#sudo docker run -d -p 8080:80 --name pg50226-drumlace-container pg50226-drumlace

sudo docker tag pg50226-drumlace asemanas/drumlace:latest
# Step 3: Push the Docker image to Docker Hub
sudo docker push asemanas/drumlace:latest