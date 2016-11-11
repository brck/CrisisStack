#!/bin/sh
#If you have not updated, kindly run this command $ apt-get update
##on ubuntu install nodejs
## on raspbian , install the node library in librariers folder.
cp /home/pi/CrisisStack/app/libraries/Etherpad-lite.conf /etc/supervisor/conf.d/Etherpad-lite.conf
service supervisor restart
