#!/bin/bash

# Updates
apt-get -y update
apt-get -y upgrade

# CTF-Platform Dependencies
apt-get -y install python3-pip nginx mongodb gunicorn git libzmq-dev nodejs-legacy npm libclosure-compiler-java ruby-dev dos2unix tmux openjdk-7-jdk

npm install -g coffee-script coffeebar react-tools jsxhint jsonlint less

pip3 install -r api/requirements.txt

gem install jekyll
gem install octopress-minify-html

# Configure Environment
echo 'PATH=$PATH:/home/easyctf/easyctf' >> /etc/profile

# Configure Nginx
cp ctf.nginx /etc/nginx/sites-enabled/ctf
rm /etc/nginx/sites-enabled/default
mkdir -p /srv/http/ctf
service nginx restart
