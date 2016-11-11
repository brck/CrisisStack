#!/bin/sh

sudo apt-get  install -y libpcre3 libpcre3-dev php5 php5-mcrypt php5-mysql php5-fpm php5-curl php5-gd php5-idn php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-mhash php5-ming php5-ps php5-pspell php5-recode php5-snmp php5-sqlite php5-tidy php5-xmlrpc php5-xsl php5-json php5-curl
sudo apt-get install -y mysql-server mysql-client
ln -s /etc/nginx/sites-available/ushahidi /etc/nginx/sites-enabled/ushahidi
service nginx restart





