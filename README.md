# Deployment Dockerized ML Models in AWS Sagemaker


## Table of contents

* [Docker](#Docker)
* [ML Docker Structure for Sagemaker](#ML-Docker-Structure-for-Sagemaker)
* [Execution Stack for Container](#Execution-Stack-for-Container)
* [WSGI (Web Server Gateway Interface)](#WSGI (Web-Server-Gateway-Interface))
* [Main Components](#Main-Components)
* [Container Application](#Container-Application)

Dataset can be found here: https://www.kaggle.com/andrewmvd/heart-failure-clinical-data

## Docker

Functionality of Docker provides a simple way to package your code into an image that is totally self-contained. After the image has been established, Docker can run a container that this image is based on. The way you set up your program is the way it runs because the containers are separated from each other and the host.

Comparing to envs like virtualenv (or conda), Docker is completely language independent and it can create the whole operating environment, including startup commands, environment variable, etc. In some ways, a Docker container is like a virtual machine, but it is much lighter weight. 


<p align="center">
  <img width="512" height="254" src=./imgs/docker.png>
</p>


## ML Docker Structure for Sagemaker

<p align="center">
  <img width="306" height="260" src=./imgs/structure.png>
</p>


### input
* /opt/ml/input/config contains information to control how your program runs. hyperparameters.json is a JSON-formatted dictionary of hyperparameter names to values. These values will always be strings, so you may need to convert them. resourceConfig.json is a JSON-formatted file that describes the network layout used for distributed training. Since scikit-learn doesn't support distributed training, we'll ignore it here.
* /opt/ml/input/data/<channel_name>/ (for File mode) contains the input data for that channel. The channels are created based on the call to CreateTrainingJob but it's generally important that channels match what the algorithm expects. The files for each channel will be copied from S3 to this directory, preserving the tree structure indicated by the S3 key structure.

### output
* /opt/ml/model/ is the directory where you write the model that your algorithm generates. Your model can be in any format that you want. It can be a single file or a whole directory tree. SageMaker will package any files in this directory into a compressed tar archive file. This file will be available at the S3 location returned in the DescribeTrainingJob result.
* /opt/ml/output is a directory where the algorithm can write a file failure that describes why the job failed. The contents of this file will be returned in the FailureReason field of the DescribeTrainingJob result. For jobs that succeed, there is no reason to write this file as it will be ignored.

## Execution Stack for Container

<p align="center">
  <img width="1222" height="481" src=./imgs/wsgi.png>
</p>

* /ping is simple health сheck endpoint that receives GET requests. If the model returns 200 (Success), then the container is up and running and ready to receive requests.
* /invocations is the endpoint that receives client inference POST requests. The format of the request and the response is up to the algorithm. 


## WSGI (Web Server Gateway Interface)

WSGI consists of two parts:

* Server part – usually web servers such as Nginx or Apache are being used
* App part – web application model created from python scripts. In case of ML models, usually there are REST-API services wrapped in a lightweight web modules such as Flask or Tornado.

The server executes the web app and sends information and a callback function to the app. The request is processed on the app side, and a response is sent back to the server utilizing the callback function.

Examples of Python frameworks that support WSGI include Django, CherryPy, Flask, TurboGears, and web2py.

<p align="center">
  <img width="1444" height="280" src=./imgs/server-app.png>
</p>

## Main Components

* Dockerfile: Document file that contains all the commands that are used when you produce an image using 'docker build'

* docker_to_ecr.sh: Shell script that builds Docker Image using Dockerfile and push that image directly to AWS ECR (Elastic Container Registry). After this procedure, this image can be used in Sagemaker for fitting the Estimator and deploying the model. Need to have preinstalled AWS CLI (Command Line Interface) and configured information using 'aws configure' command.

* sagemaker-estimator: The main working directory for ML model that you're building

## Container Application

* train: The main script that is using for training your ML models. Can also be combined with additional scripts for preprocessing, feature selection, etc.
* serve: The wrapper that is working with inference server and starts it. Usually this file stays as it is and can be used in different ml models.
* wsgi.py: Creating the start of individual workers.
* predictor.py: Model prediction script combined with flask wrapper 
* nginx.conf: Conf settings for nginx master (enabling working with multiple workers)

