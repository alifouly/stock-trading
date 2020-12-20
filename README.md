# Stock-Trading

### It consists of three parts:

  ##### 1- The 'main-app' directory:
  It includes the API which simulates parts of the stock trading process.
  ##### 2- The 'consumer-app' directory: 
  It acts the consumer container that consumes data from the data streamer and reflects on the database accordingly and update it with lates prices and availability.
  ##### 3- 'docker-compose.yml' file: 
  It is a docker.yml file that boots up the containers as it includes the 4 services; the streamer that pushes the data, the message queue, the API and the data consumer.

## To run and test the API:

  - Download the docker-compose.yml file
  - Run "docker-compose up -d" command
  - Access the API by using http://localhost:8000
  - You will find all the endpoints' documentation by accessing the following: http://localhost:8000/docs
