#!/bin/sh

# Script to turn a generic Debian Squeeze box into an Eden server
# with Apache & MySQL
# Update system
sudo apt-get update
sudo apt-get upgrade -y
# Install Admin Tools
sudo apt-get install -y unzip psmisc mlocate telnet lrzsz vim elinks-lite rcconf htop sudo
# Install Git
sudo apt-get install -y git-core
# Email
sudo apt-get -y install exim4-config exim4-daemon-light
########
# MySQL
########
sudo apt-get -y install mysql-server python-mysqldb phpmyadmin mytop
# get into superuser mode
sudo su
cd /
# Tune for smaller RAM setups

sed -i 's|query_cache_size        = 16M|query_cache_size = 1M|' /etc/mysql/my.cnf
sed -i 's|key_buffer              = 16M|key_buffer = 1M|' /etc/mysql/my.cnf
sed -i 's|max_allowed_packet      = 16M|max_allowed_packet = 1M|' /etc/mysql/my.cnf
/etc/init.d/mysql restart
#########
# Apache
#########
apt-get -y install libapache2-mod-wsgi
a2enmod rewrite
a2enmod deflate
a2enmod headers
a2enmod expires
# Enable Basic Authentication for WebServices
sed -i 's|</IfModule>|WSGIPassAuthorization On|' /etc/apache2/mods-enabled/wsgi.conf
echo "</IfModule>" >> /etc/apache2/mods-enabled/wsgi.conf
# Prevent Memory leaks from killing servers
sed -i 's|MaxRequestsPerChild   0|MaxRequestsPerChild 300|' /etc/apache2/apache2.conf
# Tune for smaller RAM setups
sed -i 's|MinSpareServers       5|MinSpareServers 3|' /etc/apache2/apache2.conf
sed -i 's|MaxSpareServers      10|MaxSpareServers 6|' /etc/apache2/apache2.conf
apache2ctl restart
# Holding Page for Maintenance windows
cat << EOF > "/var/www/maintenance.html"
<html><body><h1>Site Maintenance</h1>Please try again later...</body></html>
EOF
#########
# Python
#########
# Install Libraries
apt-get -y install libgeos-c1

apt-get -y install python-dev

apt-get -y install python-lxml python-setuptools python-dateutil
apt-get -y install python-serial
apt-get -y install python-imaging
apt-get -y install python-matplotlib
apt-get -y install python-requests
apt-get -y install python-xlwt

cd ~
wget --no-check-certificate https://pypi.python.org/packages/source/r/reportlab/reportlab-3.1.44.tar.gz
tar zxvf reportlab-3.1.44.tar.gz
cd reportlab-3.1.44
python setup.py install
cd ..

apt-get -y install libgeos-dev
wget --no-check-certificate http://pypi.python.org/packages/source/S/Shapely/Shapely-1.5.7.tar.gz
tar zxvf Shapely-1.5.7.tar.gz
cd Shapely-1.5.7
python setup.py install
cd ..
# Upgrade XLRD for XLS import support
wget --no-check-certificate https://pypi.python.org/packages/source/x/xlrd/xlrd-0.9.3.tar.gz
tar zxvf xlrd-0.9.3.tar.gz
cd xlrd-0.9.3
python setup.py install
cd ..
#########
# Web2Py
#########
apt-get -y install libodbc1
# Install Web2Py
adduser --system --disabled-password web2py
addgroup web2py
cd /home
# @ToDo: Stable release once 2.0 released
git clone --recursive git://github.com/web2py/web2py.git
ln -s /home/web2py ~
cp -f /home/web2py/handlers/wsgihandler.py /home/web2py
cat << EOF > "/home/web2py/routes.py"
#!/usr/bin/python
default_application = 'eden'
default_controller = 'default'
default_function = 'index'
routes_onerror = [
        ('eden/400', '!'),
        ('eden/401', '!'),
        ('eden/509', '!'),
        ('eden/*', '/eden/errors/index'),
        ('*/*', '/eden/errors/index'),
    ]
EOF
# Configure Matplotlib
mkdir /home/web2py/.matplotlib
chown web2py /home/web2py/.matplotlib
echo "os.environ['MPLCONFIGDIR'] = '/home/web2py/.matplotlib'" >> /home/web2py/wsgihandler.py
sed -i 's|TkAgg|Agg|' /etc/matplotlibrc
##############
# Sahana Eden
##############
# Install Sahana Eden
cd web2py
cd applications
# @ToDo: Stable branch
git clone git://github.com/flavour/eden.git
# Fix permissions
chown web2py ~web2py
chown web2py ~web2py/applications/admin/cache
chown web2py ~web2py/applications/admin/cron
chown web2py ~web2py/applications/admin/databases
chown web2py ~web2py/applications/admin/errors
chown web2py ~web2py/applications/admin/sessions
chown web2py ~web2py/applications/eden
chown web2py ~web2py/applications/eden/cache
chown web2py ~web2py/applications/eden/cron
mkdir -p ~web2py/applications/eden/databases
chown web2py ~web2py/applications/eden/databases
chown web2py ~web2py/applications/eden/errors
chown web2py ~web2py/applications/eden/models
mkdir -p ~web2py/applications/eden/sessions
chown web2py ~web2py/applications/eden/sessions
chown web2py ~web2py/applications/eden/static/fonts
chown web2py ~web2py/applications/eden/static/img/markers
mkdir -p ~web2py/applications/eden/static/cache/chart
chown web2py -R ~web2py/applications/eden/static/cache
chown web2py ~web2py/applications/eden/uploads
mkdir -p ~web2py/applications/eden/uploads/gis_cache
mkdir -p ~web2py/applications/eden/uploads/images
mkdir -p ~web2py/applications/eden/uploads/tracks
chown web2py ~web2py/applications/eden/uploads/gis_cache
chown web2py ~web2py/applications/eden/uploads/images
chown web2py ~web2py/applications/eden/uploads/tracks
ln -s /home/web2py/applications/eden ~
#####################
# Management scripts
#####################
cat << EOF > "/usr/local/bin/backup"
#!/bin/sh
NOW=\$(date +"%Y-%m-%d")
mysqldump sahana > /root/backup-\$NOW.sql
gzip -9 /root/backup-\$NOW.sql
OLD=\$(date --date='7 day ago' +"%Y-%m-%d")
rm -f /root/backup-\$OLD.sql.gz
EOF
chmod +x /usr/local/bin/backup
cat << EOF > "/usr/local/bin/compile"
#!/bin/sh
cd ~web2py
python web2py.py -S eden -M -R applications/eden/static/scripts/tools/compile.py
apache2ctl restart
EOF
chmod +x /usr/local/bin/compile
cat << EOF > "/usr/local/bin/maintenance"
#!/bin/sh
# Script to activate/deactivate the maintenance site
# Can provide the option 'off' to disable the maintenance site
if [ "\$1" != "off" ]; then
    # Stop the Scheduler
    killall python
    # Deactivate the Production Site
    a2dissite production
    # Activate the Maintenance Site
    a2ensite maintenance
else
    # Deactivate the Maintenance Site
    a2dissite maintenance
    # Activate the Production Site
    a2ensite production
    # Start the Scheduler
    cd ~web2py && sudo -H -u web2py nohup python web2py.py -K eden -Q >/dev/null 2>&1 &
fi
apache2ctl restart
EOF
chmod +x /usr/local/bin/maintenance
cat << EOF > "/usr/local/bin/pull"
#!/bin/sh
cd ~web2py/applications/eden
sed -i 's/settings.base.migrate = False/settings.base.migrate = True/g' models/000_config.py
git pull
/usr/local/bin/maintenance
rm -rf compiled
cd ~web2py
sudo -H -u web2py python web2py.py -S eden -M -R applications/eden/static/scripts/tools/noop.py
cd ~web2py/applications/eden
sed -i 's/settings.base.migrate = True/settings.base.migrate = False/g' models/000_config.py
/usr/local/bin/compile
/usr/local/bin/maintenance off
EOF
chmod +x /usr/local/bin/pull
# Change the value of prepopulate, if-necessary
cat << EOF > "/usr/local/bin/clean"
#!/bin/sh
/usr/local/bin/maintenance
cd ~web2py/applications/eden
rm -f databases/*
rm -rf errors
rm -rf sessions
rm -rf uploads
sed -i 's/settings.base.migrate = False/settings.base.migrate = True/g' models/000_config.py
sed -i 's/settings.base.prepopulate = 0/#settings.base.prepopulate = 0/g' models/000_config.py
rm -rf compiled
mysqladmin -f drop sahana
mysqladmin create sahana
cd ~web2py
sudo -H -u web2py python web2py.py -S eden -M -R applications/eden/static/scripts/tools/noop.py
cd ~web2py/applications/eden
sed -i 's/settings.base.migrate = True/settings.base.migrate = False/g' models/000_config.py
sed -i 's/#settings.base.prepopulate = 0/settings.base.prepopulate = 0/g' models/000_config.py
/usr/local/bin/maintenance off
/usr/local/bin/compile
EOF
chmod +x /usr/local/bin/clean
cat << EOF > "/usr/local/bin/w2p"
#!/bin/sh
cd ~web2py
python web2py.py -S eden -M
EOF
chmod +x /usr/local/bin/w2p
# END


#!/bin/sh
# Script to configure an Eden server
# - assumes that install-eden-apache-mysql.sh has been run
echo -e "What domain name should we use? : \c "
read DOMAIN
echo -e "What host name should we use? : \c "
read hostname
sitename=$hostname".$DOMAIN"
echo -e "What is the current root MySQL password: \c "
read rootpw
# @ToDo: Generate a random password
echo Note that web2py will not work with passwords with an @ in them
echo -e "What should be the MySQL password for user 'sahana'? \c "
read password
echo "Now reconfiguring system"
cd /etc
filename="hosts"
sed -i "s|localdomain localhost|localdomain localhost $hostname|" $filename
cd /etc
filename="hostname"
echo $hostname > $filename
cd /etc
filename="mailname"
echo $sitename >  $filename
# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------
echo configure for Internet mail delivery
dpkg-reconfigure exim4-config
# -----------------------------------------------------------------------------
# Update system
#   in case run at a much later time than the install script
# -----------------------------------------------------------------------------
apt-get update
apt-get upgrade -y
cd ~web2py/applications/eden
git pull
# -----------------------------------------------------------------------------
# Apache Web server
# -----------------------------------------------------------------------------
echo "Setting up Web server"
rm -f /etc/apache2/sites-enabled/000-default
cat << EOF > "/etc/apache2/sites-available/production"
<VirtualHost *:80>
  ServerName $hostname.$DOMAIN
  ServerAdmin webmaster@$DOMAIN
  DocumentRoot /home/web2py/applications
  WSGIScriptAlias / /home/web2py/wsgihandler.py
  ## Edit the process and the maximum-requests to reflect your RAM
  WSGIDaemonProcess web2py user=web2py group=web2py home=/home/web2py processes=4 maximum-requests=100
  RewriteEngine On
  # Stop GoogleBot from slowing us down
  RewriteRule .*robots\.txt$ /eden/static/robots.txt [L]
  # extract desired cookie value from multiple-cookie HTTP header
  #RewriteCond %{HTTP_COOKIE} registered=([^;]+)
  # check that cookie value is correct
  #RewriteCond %1 ^yes$
  #RewriteRule ^/$ /eden/ [R,L]
  #RewriteRule ^/$ /eden/static/index.html [R,L]
  RewriteCond %{REQUEST_URI}    !/phpmyadmin(.*)
  RewriteCond %{REQUEST_URI}    !/eden/(.*)
  RewriteRule /(.*) /eden/$1 [R]
  ### static files do not need WSGI
  <LocationMatch "^(/[\w_]*/static/.*)">
    Order Allow,Deny
    Allow from all
    SetOutputFilter DEFLATE
    BrowserMatch ^Mozilla/4 gzip-only-text/html
    BrowserMatch ^Mozilla/4\.0[678] no-gzip
    BrowserMatch \bMSIE !no-gzip !gzip-only-text/html
    SetEnvIfNoCase Request_URI \.(?:gif|jpe?g|png)$ no-gzip dont-vary
    Header append Vary User-Agent env=!dont-vary
    ExpiresActive On
    ExpiresByType text/html "access plus 1 day"
    ExpiresByType text/javascript "access plus 1 week"
    ExpiresByType text/css "access plus 2 weeks"
    ExpiresByType image/ico "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType application/x-shockwave-flash "access plus 1 month"
  </LocationMatch>
  ### everything else goes over WSGI
  <Location "/">
    Order deny,allow
    Allow from all
    WSGIProcessGroup web2py
  </Location>
  ErrorLog /var/log/apache2/$hostname_error.log
  LogLevel warn
  CustomLog /var/log/apache2/$hostname_access.log combined
</VirtualHost>
EOF
a2ensite production
apache2ctl restart
cat << EOF > "/etc/apache2/sites-available/maintenance"
<VirtualHost *:80>
  ServerName $hostname.$DOMAIN
  ServerAdmin webmaster@$DOMAIN
  DocumentRoot /var/www
  RewriteEngine On
  RewriteCond %{REQUEST_URI} !/phpmyadmin(.*)
  RewriteRule ^/(.*) /maintenance.html
  <Location "/">
    Order deny,allow
    Allow from all
  </Location>
  ErrorLog /var/log/apache2/maintenance_error.log
  LogLevel warn
  CustomLog /var/log/apache2/maintenance_access.log combined
</VirtualHost>
EOF
# -----------------------------------------------------------------------------
# MySQL Database
# -----------------------------------------------------------------------------
echo "Setting up Database"
# Allow root user to access database without entering password
cat << EOF > "/root/.my.cnf"
[client]
user=root
EOF
echo "password='$rootpw'" >> "/root/.my.cnf"
# Create database
mysqladmin create sahana
# Create user for Sahana application
echo "CREATE USER 'sahana'@'localhost' IDENTIFIED BY '$password';" > "/tmp/mypass"
echo "GRANT ALL PRIVILEGES ON *.* TO 'sahana'@'localhost' WITH GRANT OPTION;" >> "/tmp/mypass"
mysql < /tmp/mypass
rm -f /tmp/mypass
# Schedule backups for 02:01 daily
echo "1 2   * * * * root    /usr/local/bin/backup" >> "/etc/crontab"
# -----------------------------------------------------------------------------
# Sahana Eden
# -----------------------------------------------------------------------------
echo "Setting up Sahana"
# Copy Templates
cp ~web2py/applications/eden/modules/templates/000_config.py ~web2py/applications/eden/models
sed -i 's|EDITING_CONFIG_FILE = False|EDITING_CONFIG_FILE = True|' ~web2py/applications/eden/models/000_config.py
sed -i "s|akeytochange|$sitename$password|" ~web2py/applications/eden/models/000_config.py
sed -i "s|127.0.0.1:8000|$sitename|" ~web2py/applications/eden/models/000_config.py
sed -i 's|base.cdn = False|base.cdn = True|' ~web2py/applications/eden/models/000_config.py
# Configure Database
sed -i 's|#settings.database.db_type = "mysql"|settings.database.db_type = "mysql"|' ~web2py/applications/eden/models/000_config.py
sed -i "s|#settings.database.password = \"password\"|settings.database.password = \"$password\"|" ~web2py/applications/eden/models/000_config.py
# Create the Tables & Populate with base data
sed -i 's|settings.base.prepopulate = 0|settings.base.prepopulate = 1|' ~web2py/applications/eden/models/000_config.py
sed -i 's|settings.base.migrate = False|settings.base.migrate = True|' ~web2py/applications/eden/models/000_config.py
cd ~web2py
sudo -H -u web2py python web2py.py -S eden -M -R applications/eden/static/scripts/tools/noop.py
# Configure for Production
sed -i 's|settings.base.prepopulate = 1|settings.base.prepopulate = 0|' ~web2py/applications/eden/models/000_config.py
sed -i 's|settings.base.migrate = True|settings.base.migrate = False|' ~web2py/applications/eden/models/000_config.py
cd ~web2py
sudo -H -u web2py python web2py.py -S eden -M -R applications/eden/static/scripts/tools/compile.py
# Add Scheduler
sed -i 's|exit 0|cd ~web2py \&\& python web2py.py -K eden -Q >/dev/null 2>\&1 \&|' /etc/rc.local
echo "exit 0" >> /etc/rc.local
#read -p "Press any key to Reboot..."
echo "Now rebooting.."
reboot
# END
