#!/bin/bash
DATA_DIR=/opt/data
echo "[-] Provisioning: $DATA_DIR"
###
# Setup mountpoints
mkdir -p $DATA_DIR
parted -s /dev/vdb -- mklabel msdos
parted -s /dev/vdb -- mkpart primary ext4 0 -1
mkfs.ext4 /dev/vdb1
mount -t ext4 /dev/vdb1 $DATA_DIR
###
# Install crap
dnf install -y docker git polkit words
sed -i "s,DOCKER_STORAGE_OPTIONS=,DOCKER_STORAGE_OPTIONS=-g $DATA_DIR," /etc/sysconfig/docker-storage
systemctl enable docker
systemctl start docker
git clone https://github.com/docker/distribution.git /opt/ims/distribution
cd /opt/ims/distribution
docker build -t dist .
echo "[!] Provisioning done!"
