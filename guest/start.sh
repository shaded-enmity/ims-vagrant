#!/bin/bash
PERMUTER=/opt/ims/docker-image-permuter.py
LOCALURL='127.0.0.1:8080'

# Permuter creates one repo per invocation
for I in $(seq ${1:-1}); do
        $PERMUTER $LOCALURL | tee -a image_names
done

for IMG in $(cat image_names); do
        docker push $IMG
done
