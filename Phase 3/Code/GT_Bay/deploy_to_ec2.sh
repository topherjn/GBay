#!/usr/bin/env bash
PEM_KEY=/Users/danhiggins/Code/AWS/keys/Tomcat-key.pem

if [ "$1" == "" ]; then
    echo no ec2 address passed! usage: deploy_to_ec2.sh ubuntu@34.206.176.170
    exit
else
    cd /Users/danhiggins/Code/GATech/CS6400_Database_Design/6400Spring18Team047/Code/GT_Bay
    tar -cvf gt_bay.tar gt_bay
    scp -i ${PEM_KEY} gt_bay.tar ${1}:/home/ubuntu/Applications/
    ssh -i ${PEM_KEY} $1 'cd /home/ubuntu/Applications/gt_bay; kill -9 `cat gunicorn.pid`'|| :
    ssh -i ${PEM_KEY} $1 'cd /home/ubuntu/Applications; rm -rf gt_bay'|| :
    ssh -i ${PEM_KEY} $1 'cd /home/ubuntu/Applications; tar -xvf gt_bay.tar'
fi

