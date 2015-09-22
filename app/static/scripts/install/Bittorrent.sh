#!/bin/sh 
sudo apt-get install software-properties-common python-software-properties -y 
apt-key adv --keyserver keys.gnupg.net --recv-keys 6BF18B15 -y 
CODENAME=$(lsb_release -cs | sed -n '/lucid\|precise\|quantal\|raring\|saucy\|trusty\|squeeze\|wheezy\|jessie\|sid/p')
echo "" >> /etc/apt/sources.list
echo "#### BitTorrent Sync - see: http://forum.bittorrent.com/topic/18974-debian-and-ubuntu-server-packages-for-bittorrent-sync-121-1/" >> /etc/apt/sources.list
echo "## Run this command: apt-key adv --keyserver keys.gnupg.net --recv-keys 6BF18B15" >> /etc/apt/sources.list
echo "deb http://debian.yeasoft.net/btsync ${CODENAME:-sid} main" >> /etc/apt/sources.list
echo "deb-src http://debian.yeasoft.net/btsync ${CODENAME:-sid} main" >> /etc/apt/sources.list
unset CODENAME
apt-get update
apt-get -y install btsync

#touch /etc/btsync/samba.conf
#//!/usr/lib/btsync/btsync-daemon --config

#// This btsync configuration file shows how to configure a btsync
#// instance running under specific user credentials and/or how
#// to supply additional configuration parameters.
#//
#// Configuration parameters not parsed by btsync but by the daemon
#// init script can be supplied as comments in the configuration file.
#//
#// The following parameters are supported:
#//
#// DAEMON_UID:      A uid for supplying the user under which
#//                  the btsync daemon should run
#//
#// DAEMON_GID:      A gid for supplying the group under which
#//                  the btsync daemon should run. If omitted
#//                  the daemon will run under the primary group
#//                  of the user
#//
#// DAEMON_UMASK:    The umask (up to 4 octal digits) for the
#//                  btsync daemon. If omitted the default umask
#//                  is used.
#//
#// DAEMON_DEBUG:    The debug mask (4 hex digits) for the btsync
#//                  daemon. If omitted the init script will not
#//                  touch potential settings defined manually.
#//                  If set to 0000, a potential settings file
#//                  will be deleted. Full detail is set by
#//                  specifying FFFF
#//
#// The parameter definition must use an equal sign ("="):
#//
#// DAEMON_UID=samba
#// DAMONE_GID=samba
#// DAEMON_UMASK=0022
#//
#// This example will launch the instance running under the credentials
#// of the user "samba" using 0022 as umask
#// The internal data of the btsync daemon will be written in
#// /home/samba/.btsync
#//
# {
#        "device_name": "SMB btsync Server",
#        "listening_port" : 0,
#        "storage_path" : "/home/samba/.btsync",
#        "check_for_updates" : false,
#        "use_upnp" : true,
#        "download_limit" : 0,
#        "upload_limit" : 0, 
#        "webui" :
#        {
#                "listen" : "0.0.0.0:8888",
#                "login" : "admin",
#                "password" : "Password"
#        }
#}

sudo service btsync restart 