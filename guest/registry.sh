#!/bin/bash

sudo docker run -dp 8080:5000 -v /opt/data/cache:/var/lib/registry:Z dist
