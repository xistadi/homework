#!/bin/bash


#1configure network to have ssh access from local machine;
#Configuring Network Interface for DHCP
sed -i 's/ONBOOT=no/ONBOOT=yes/' /etc/sysconfig/network-scripts/ifcfg-enp0s? && echo SUCCESS change ONBOOT=no to yes
systemctl restart NetworkManager.service && echo SUCCESS network restart
#SSH
yum -y install openssh-server openssh-clients && echo SUCCESS install openssh
chkconfig sshd on && echo SUCCESS sshd on
service sshd start && echo SUCCESS sshd start


#restrict ssh connections for root user and to single ssh port(iptables);
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && echo SUCCESS change PermitRootLogin to no
service sshd restart && echo SUCCESS sshd restart


#add local DVD ISO as an repo(all internet repos need to be removed);
yum -y install wget && echo SUCCESS install wget
wget -P /home http://mirror.datacenter.by/pub/CentOS/7.9.2009/isos/x86_64/CentOS-7-x86_64-DVD-2009.iso && echo SUCCESS download iso
mkdir /cdrom && echo SUCCESS mkdir
mount /home/CentOS-7-x86_64-DVD-2009.iso /cdrom && echo SUCCESS mount
rm -f /etc/yum.repos.d/*.repo && echo SUCCESS remove all repos
echo -e '[LocalRepo]
name=Local Repository
baseurl=file:///cdrom
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7' > /etc/yum.repos.d/local.repo && echo SUCCESS created local.repo
yum clean all && echo SUCCESS yun clean
