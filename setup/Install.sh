#!/bin/sh

# Update
apt-get update
apt-get upgrade

# Install apache
apt-get install -y apache2

# Install PHP
apt-get install -y php5 php5-cli

# Install Python and IDLE
sudo apt-get install -y python python-dev python2.7 python2.7-dev idle python-serial python-numpy

# Install Cython for compiling Python in C
sudo apt-get install -y cython

# Set web permissions for www-data
groupadd www-data
usermod -g www-data www-data
chown -R www-data:www-data /var/www

# Mount web directory for udooer to edit (installs bindfs)
apt-get -y install bindfs

mkdir -p /home/udooer/hyperloop
mkdir -p /home/udooer/hyperloop/web
chown -Rf udooer:udooer /home/udooer/hyperloop
chmod -Rf 770 /home/udooer/hyperloop

