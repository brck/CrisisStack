# CrisisStack

This is the development branch to cater for revision.

The software stack is an application store that allows you to install and launch various applications first release(Primary set) for first Crisis responders. Some of the applications included are:

* Etherpad-lite [(Github)](http://github.com/ether/etherpad-lite): A real-time collaborative document editing tool.

* Ushahidi [(Github)](https://github.com/ushahidi/Ushahidi_Web): A platform that allows information collection, visualization and interactive mapping allowing anyone to submit information through text messaging using a mobile phone,email or web form

* Sahana Eden [(Official Site)](http://sahanafoundation.org/products/eden/): A suite of tools designed specifically for organizations during disasters, including organization registry, project tracking, asset tracking and more.

* BitTorrent Sync [(Official Site)](https://www.getsync.com/) -Fast, simple, and secure file syncing for IT and individuals.

In progress:

* OSM Sync [(Blog)](https://blog.openstreetmap.org/2013/04/29/openstreetmap-opens-up-to-more-contributors-with-easy-add-a-note-feature/) – Make a mark on a map served off the BRCK+Pi and synchronize with OSM API occasionally

More software shall be optimized and/or added over time.

# Installation

System Requirements
--------------------
We have included a set of packages in our image that allow you to install these applications, where most of them share libraries that can be viewed from the individual package install scripts.
If you wish to see what is required to launch a particular application please visit that the specific package.

For the application store please view the install notes on the website to get the latest information.


Setting Up Your Development Environment
----------------------------------------

Crisis Stack has been written in python using the Flask framework and MySQL DataBase.
You will therefore need to set up a local development environment on your machine and installing a virtual environment.

Update your sources by punching in the following command:
    sudo apt-get update
    sudo apt-get -y upgrade

Install the following packages:

For instructions on how to install MySQL visit [Install MySQL on Ubuntu](https://www.linode.com/docs/databases/mysql/install-mysql-on-ubuntu-14-04)

Python comes installed with ubuntu and other linux based systems.

Setting Up Your Virtual Environment
-----------------------------------
To have a virtual environment install virtualenv from pip globally.
```bash
sudo pip install virtualenv
```

Next navigate to your preferred location where our project will reside. You will then need to browse to any location on your machine where you have write permission. I would recommend your home directory.
You can access it by issuing the following command.

    cd ~

Proceed to clone the repository by issuing the following command:

    git clone git@github.com:brck/CrisisStack.git

You will now have a directory labelled CrisisStack

    cd CrisisStack

Create a Virtual Environment using the following command. This will jail your development environment. In my case I call my virtual environment 'venv'. You can call it any other name your preffer:

    virtualenv venv

You then need to activate it by issuing either of the following commands:

    . venv/bin/acticate
or

    source venv/bin/activate

Proceed to Install the packages listed in requirements.txt or by issuing the following command:

    pip install -r requirements.txt

You can now start the application. For more information on how to use virtual environments visit [Virtual Environments Docs](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Configuration
-------------
The config.py file under the project root contains different Configuration classes for different environments.
*   Config - Is the base configuration that all others classes inherit and use. Some options can be overwritten based on the environment.

Since the application uses settings stored in the environment, you need to set them using the export command. For example to setup the database url used by SQLAlchemy in development:

    export DEV_DATABASE_URL="mysql://username:password@localhost/crisis_stack"

Replacing "username" and "password" with your database username and password respectively.

Flask uses the SECRET_KEY variable to ensure security. For the application to work properly you need to set this. You can generate the secret key by punching the following code snippet in the python shell.
```python
>>> import os
>>> os.urandom(24)
```
Copy the resulting string so as to set the SECRET_KEY variable.

    export SECRET_KEY="GENERATED_KEY"

To run code coverage of the tests, you need to specify another environment variable 'FLASK_COVERAGE' to activate coverage. First set the variable as below:

    export FLASK_COVERAGE="1"

Now you can run tests under coverage using

    python manage.py test

Otherwise to run normal tests just run the above command without setting the FLASK_COVERAGE variable.

Running the application
-----------------------
To run the application first we need to perform database migrations to create database tables and initialize the tables with default applications. Run the following command from the terminal while at the root directory of the application.

    python manage.py db init_app

After upgrading start the application as Below

    python manage.py runserver

Once the sever is up and running you can now visit your browser with the url below.

    127.0.0.1:5000/

Have fun!!!!
