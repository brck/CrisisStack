#!/bin/sh

sudo apt-get  install -y libpcre3 libpcre3-dev php5 php5-mcrypt php5-mysql php5-curl php5-gd php5-idn php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-mhash php5-ming php5-ps php5-pspell php5-recode php5-snmp php5-sqlite php5-tidy php5-xmlrpc php5-xsl php5-json php5-curl
sudo apt-get install -y mysql-server mysql-client


echo -n "Enter the MySQL root password: "
read -s rootpw
echo -n "Enter database name: "
read dbname
echo -n "Enter database username: "
read dbuser
echo -n "Enter database user password: "
read dbpw
 
db="create database $dbname;GRANT ALL PRIVILEGES ON $dbname.* TO $dbuser@localhost IDENTIFIED BY '$dbpw';FLUSH PRIVILEGES;"
mysql -u root -p$rootpw -e "$db"
 
if [ $? != "0" ]; then
 echo "[Error]: Database creation failed"
 exit 1
else
 echo "------------------------------------------"
 echo " Database has been created successfully "
 echo "------------------------------------------"
 echo " DB Info: "
 echo ""
 echo " DB Name: $dbname"
 echo " DB User: $dbuser"
 echo " DB Pass: $dbpw"
 echo ""
 echo "------------------------------------------"
fi



 
cd ~
git clone https://github.com/ushahidi/Ushahidi_Web.git
mv Ushahidi_Web /var/www/
cd /var/www/Ushahidi_Web

sudo chmod -R 777 application/config 
sudo chmod -R 777 application/cache
sudo chmod -R 777 application/logs
sudo chmod -R 777 media/uploads
sudo chmod 777 .htaccess

sudo cd /etc/apache2/sites-available/

sudo a2ensite ushahidi




