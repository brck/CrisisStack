#!/bin/sh 
sudo apt-get update 
sudo apt-get -y  install libraries/node-arm.deb
sudo apt-get -y install gzip git-core curl libssl-dev pkg-config build-essential npm
cd ~
mkdir applications && cd applications 
git clone https://github.com/ether/etherpad-lite
cd etherpad-lite
npm install dirty && npm update
./bin/run.sh