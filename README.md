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
At the time of writing this, these are some of the packages I had in my virtual environment: 
``` Babel==2.0
	Flask==0.10.1
	Flask-Babel==0.9
	Flask-JSON==0.2.0
	Flask-Login==0.2.11
	Flask-Mail==0.9.1
	Flask-OpenID==1.2.4
	Flask-SQLAlchemy==2.0
	Flask-WTF==0.12
	Flask-WhooshAlchemy==0.56
	Jinja2==2.8
	MarkupSafe==0.23
	SQLAlchemy==1.0.8
	Tempita==0.5.2
	WTForms==2.0.2
	Werkzeug==0.10.4
	Whoosh==2.7.0
	argparse==1.2.1
	blinker==1.4
	coverage==3.7.1
	decorator==4.0.2
	flipflop==1.0
	guess-language==0.2
	itsdangerous==0.24
	pbr==1.7.0
	python-openid==2.2.5
	pytz==2015.4
	six==1.9.0
	speaklater==1.3
	sqlalchemy-migrate==0.10.0
	sqlparse==0.1.16
	wsgiref==0.1.2 
``` 

Please note that the numbers indicate the package versions.

You can now start the application by executing the following command: 

``` python run.py ```

Have fun!!!! 




