# CrisisStack
This is the development branch to cater for revision. 

The software stack is an application store that allows you to install and launch various applciations that are we consider a first release(Primary set) for first Crisis responders. Some of the applications included are:

*Etherpad-lite (http://github.com/ether/etherpad-lite): A real-time collaborative document editing tool. 

*Ushahidi(https://github.com/ushahidi/Ushahidi_Web):A platform that allows information collection, visialuzation and interactive mapping 
allowing anyone to submit information through text messaging using a mobile phone,email or web form

*Sahana Eden(http://sahanafoundation.org/products/eden/) : A suite of tools designed specifically for organizations during disasters, including organization registry, project tracking, asset tracking and more.

*OSM Sync(https://blog.openstreetmap.org/2013/04/29/openstreetmap-opens-up-to-more-contributors-with-easy-add-a-note-feature/) – Make a mark on a map served off the BRCK+Pi and synchronize with OSM API occasionally

More software shall be optimized and/or added over time. 

System Requirements 
--------------------
We have included a set of packages in our image that allow you to install these applications, where most of them share libraries that can be viewed from the individual package install scripts. 
If you wish to see what is required to launch a particular app please visit that the specific package. 

For the application store please view the install notes on the website to get the latest information. 


Setting Up Your Development Environment 
----------------------------------------

This application has mainly been written in python using the Flask framework. 
You will therefore need to set up a local develoopment environment on your machine. Below are instructions on how to do this on Ubuntu. 

Update your sources by punching in the following command: 

``` sudo apt-get update ```
``` sudo apt-get -y upgrade ```

Install the following packages: 

``` sudo apt-get -y install linux-headers wget wget python apache libapache2-mod-wsgi perl git wget python-pip postgresql-contrib postgresql build-essential gdb cython python-virtualenv ```

You will then need to browse to any location on your machine where you have write permission. I would recommend your home directory. 
You can access it by issuing the following command. 

```cd ~ ```

Proceed to clone the repository by issuing the following command: 

``` git clone git@github.com:brck/CrisisStack.git ```

You will now have a directory labelled CrisisStack 
 ``` cd CrisisStack ```

Create a Virtual Environment using the following command. This will jail your development environment. In my case I call my virtual environment flask. You can call it any other name your preffer: 

```  virtualenv flask ```

You then need to activate it by issuing either of the following commands:

``` . flask/bin/acticate ```

or 

``` source flask/bin/activate ```

Proceed to Install the packages listed in requirements.txt or by issuing the following command:

pip install flask flask-login flask-openid flask-mail flask-sqlalchemy sqlalchemy-migrate flask-whooshalchemy flask-wtf flask-babel guess_language flipflop coverage flask-json

The packages above will be specific to your virtual environment.  




