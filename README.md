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
To have a virtual environment install virtualenv from pip globally
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

You can now start the application.

Running the application
-----------------------
To run the application first we need to perform database migrations to create database tables. Run the following command from the terminal while at the root directory of the application.

    python manage.py db upgrade

After upgrading start the application as Below

    python manage.py runserver

Once the sever is up and running you can now visit your browser with the url Below

    127.0.0.1:5000/

Have fun!!!!
