#Etherpad lite on the BRCK-PI

This guide shall take you through the installation and configuration of etherpad-lite on the BRCK-PI
This is part of the stack that has been described on the README.md on the repo. 

System Requirements 
--------------------

To install the platform on your PI the following software libraries must be installed:

Java Runtime Enviroment 
Nodejs libraries 

If you have download an installation image from our library then it comes packaged with the Java Runtime Environment. 
If you have an image of a different source, please follow [these instructions](http://docs.oracle.com/javase/7/docs/webnotes/install/linux/linux-jre.html) to get the JRE up and running. 

You can then install the nodejs librries to your image. You can either compile from source, download one for your specific distribution or use the one we have provided in this repo. 
After downloading it to your pi, execute the following command to install it. Please ensure you are in the same directory as the package before executing this command. 

``` dpkg -i node-arm.deb ```

Required Libraries 

-------------------
You will also require the following software libraries to get etherpad-lite working smoothly. 
*gzip 
*git-core 
*curl 
*libssl-dev 
*pkg-config 
*build-essential 
*npm

These can be installed by running the following command:
```sudo apt-get install gzip git-core curl libssl-dev pkg-config build-essential npm ```

Cloning Etherpad Repo
----------------------

You now need to clone the repo. Before we do that let us make sure we are in our home directory. You can do this by executing the following command: 

cd ~

You then need to clone the repo by executing the following command: 

```git clone https://github.com/ether/etherpad-lite```



