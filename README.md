# CrisisStack
This is the lua development branch to cater for revision of the local application. 

The software stack is an application store that allows you to install and launch various applciations that are we consider a first release(Primary set) for first Crisis responders. Some of the applications included are:

* Etherpad-lite (http://github.com/ether/etherpad-lite): A real-time collaborative document editing tool. 

* Ushahidi(https://github.com/ushahidi/Ushahidi_Web):A platform that allows information collection, visialuzation and interactive mapping 
allowing anyone to submit information through text messaging using a mobile phone,email or web form

* Sahana Eden(http://sahanafoundation.org/products/eden/) : A suite of tools designed specifically for organizations during disasters, including organization registry, project tracking, asset tracking and more.

* BitTorrent Sync(https://www.getsync.com/) -Fast, simple, and secure file syncing for IT and individuals.

In progress: 

* OSM Sync(https://blog.openstreetmap.org/2013/04/29/openstreetmap-opens-up-to-more-contributors-with-easy-add-a-note-feature/) – Make a mark on a map served off the BRCK+Pi and synchronize with OSM API occasionally

More software shall be optimized and/or added over time. 

System Requirements 
--------------------
This is a package that allows you to manage your device locally. 


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




