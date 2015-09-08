# CrisisStack
This guide shall take you through how to install the criris stack software on the BRCK+PI MRTR. 

The software stack currently includes:
Etherpad-lite (http://github.com/ether/etherpad-lite): A real-time collaborative document editing tool. 
Ushahidi(https://github.com/ushahidi/Ushahidi_Web):A platform that allows information collection, visialuzation and interactive mapping allowing anyone to submit information through text messaging using a mobile phone,email or web form

More software shall be optimized and/or added over time. 

System Requirements 
--------------------

To install the platform on your PI the following software libraries must be installed:

*php version 5.3 or greater
*MySQL version 5.0 or greater 
*An web server 
*unicode support in the operating system

Required Extensions
-------------------
In addition to the software mentioned above please install these php libraries. The commands have been given below. 

* [PCRE](http://php.net/pcre)
* [iconv](http://php.net/iconv)
* [mycrype](http://php.net/mcrypt)
* [mbstring](http://php.net/mbstring)
* [cURL](http://php.net/curl)
* [MySQL](http://php.net/mysql)
* [IMAP](http://php.net/imap)
* [GD](http://php.net/gd)

The command is

  ```sudo apt-get -y install libpcre3 libpcre3-dev iconv php5-mcrypt php5-mysql php5-curl php5-gd php5-idn php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-mhash php5-ming php5-ps php5-pspell php5-recode php5-snmp php5-sqlite php5-tidy php5-xmlrpc php5-xsl php5-json php5-curl ```

Installation
------------
* #####Download and extract Ushahidi 
   There are two recommended ways to do this: 
   
   You can obtain ushahidi from the official realease site which is available [here](http://download.ushahidi.com).
   
   
   You may also choose to download it from the [Ushahidi github repo](https://github.com/ushahidi/Ushahidi_Web)
   
If you chose to go with the first option kindly proceed to unpack the files as shown below :
On Linux

	tar -xzvf Ushahidi-web-xxxx-tar.gz

or if it is a zip file 

	unzip Ushahidi-web-xxxx.zip

You will then need to move the directory to your public HTML directory. 
In this case, we moved the contents of the directory to /var/www/

* #####Permissions 
     We then need to ensure that the directory is writable by setting the permissions as follows:

    ```
    cd var/www/
    chmod -R 777 application/config
    chmod -R 777 application/cache
    chmod -R 777 application/logs
    chmod -R 777 media/uploads
    chmod 777 .htaccess 

    ```

* ####Create the ushahidi database 
  
  Ushahidi strores all its data in a database . We need to create a user account on the database management system and then proceed to give the user rights to access the database we shall be creating.  

Proceed to log in as the root user. The root password is the one you input when you installed mysql-server earlier. 

Input the following command to create the new user:

  ```CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';```

You then need to give the new user read and write access to the database management system. You do this by executing the following command:
  
  ```GRANT ALL PRIVILEGES ON *.* TO 'user' @ 'localhost' WITH GRANT OPTION```

However, if you want to only grant the user read and write access to that database then please use the command below.

  ```GRANT SELECT INSERT, DELETE, UPDATE, CREATE, DROP, ALTER, INDEX, LOCK ON TABLES On database.* TO 'user'@'localhost';```

RUN THE INSTALL SCRIPT 
----------------------

To run the install script, point your browser to the base URL of your raspberry pi.This will then allow you to set up your instance.  

Cleaning up 
-----------

Now that we are done, we need to remove the installation files. 
You can do this by issuing the following commands:

```
cd /var/www
chmod -R 755 application/config 
chmod 644 application/config/*
chmod 644 *.htaccess

```


