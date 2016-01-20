# CrisisStack
This is the lua development branch to cater for revision of the local application. 

The software stack is an device management web app that allows you to: 
* launch various applciations that are available on the open store. 
* Manage your device 

More features shall be optimized and/or added over time. 

System Requirements 
--------------------
This is a package that allows you to manage your device locally. 
* Ubuntu snappy core 
* 1GB of RAM 
* 1.0GHZ processor 

Setting Up Your Development Environment 
----------------------------------------

This application is to be written in mainly been written in lua using the lapis framework. 

Update your sources by punching in the following command: 

* ``` sudo apt-get update ```

* ``` sudo apt-get -y upgrade ```

You can then install the following packages that are required for development and running of the application: 

* ``` sudo apt-get -y install luarocks autotools-dev libltdl-dev liblua5.1-0 liblua5.1-0-dev libreadline-dev libreadline6-dev libtinfo-dev libtool lua5.1 zip   libtool-doc autoconf automaken gfortran fortran95-compiler gcj-jdk ```

* ``` sudo luarocks install lapis ```


TBD
----
For more on setting up your development environment please look through Dev-Environ.txt




