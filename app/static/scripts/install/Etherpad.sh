#!/bin/sh 
sudo apt-get update 
sudo apt-get install libraries/node-arm.deb
sudo apt-get install gzip git-core curl libssl-dev pkg-config build-essential npm
cd /applications 
git clone https://github.com/ether/etherpad-lite
cd etherpad-lite
npm install dirty && npm update
./bin/run.sh