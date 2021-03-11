#!/bin/bash


#1configure network to have ssh access from local machine;
#Configuring Network Interface for DHCP
sed -i 's/ONBOOT=no/ONBOOT=yes/' /etc/sysconfig/network-scripts/ifcfg-enp0s3 #change ONBOOT=no to yes
sed -i 's/ONBOOT=no/ONBOOT=yes/' /etc/sysconfig/network-scripts/ifcfg-enp0s8 #change ONBOOT=no to yes
systemctl restart NetworkManager.service #network restart

#SSH
yum -y install openssh-server openssh-clients
chkconfig sshd on 
service sshd start 

#restrict ssh connections for root user and to single ssh port(iptables);
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config  