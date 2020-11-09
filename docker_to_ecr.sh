#!/usr/bin/env bash

image=$1

if [ "$image" == "" ]
then
    echo "Usage: $0 <image-name>"
    exit 1
fi

chmod +x sagemaker-estimator/trainer
chmod +x sagemaker-estimator/server

account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi


region=$(aws configure get region)
region=${region:-eu-west-1}


fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

aws ecr describe-repositories --repository-names "${image}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${image}" > /dev/null
fi

$(aws ecr get-login --region ${region} --no-include-email)


docker build  -t ${image} .
docker tag ${image} ${fullname}

docker push ${fullname}
