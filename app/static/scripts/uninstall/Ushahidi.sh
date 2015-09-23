#!/bin/sh 
cd /etc/apache2/sites-available/ 
sudo a2dissite Ushahidi 
sudo service apache2 restart
