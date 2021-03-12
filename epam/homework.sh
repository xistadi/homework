#!/bin/bash


# configure network to have ssh access from local machine;
# Configuring Network Interface for DHCP
sed -i 's/ONBOOT=no/ONBOOT=yes/' /etc/sysconfig/network-scripts/ifcfg-enp0s? && echo SUCCESS change ONBOOT=no to yes
systemctl restart NetworkManager.service && echo SUCCESS network restart
# SSH
yum -y install openssh-server openssh-clients && echo SUCCESS install openssh
chkconfig sshd on && echo SUCCESS sshd on
service sshd start && echo SUCCESS sshd start


# restrict ssh connections for root user and to single ssh port(iptables);
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && echo SUCCESS change PermitRootLogin to no
service sshd restart && echo SUCCESS sshd restart
iptables -A INPUT -p tcp --dport 22 -j ACCEPT && echo SUCCESS single ssh port


# add local DVD ISO as an repo(all internet repos need to be removed);
yum -y install wget && echo SUCCESS install wget
# wget -P /home http://mirror.datacenter.by/pub/CentOS/7.9.2009/isos/x86_64/CentOS-7-x86_64-DVD-2009.iso && echo SUCCESS download iso
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


# set up RAID5 on 3 more drives(the size is not matter);
yum install mdadm -y && echo SUCCESS install mdamd
mdadm --create /dev/md5 --level=5 --raid-devices=3 /dev/sd[b-d]1 && echo SUCCESS create md device
mkfs.ext4 /dev/md5 && echo SUCCESS create file system for raid devices
mkdir /raid5 && echo SUCCESS create a mount point directory named raid5
tempUUID=$(blkid /dev/md5 | cut -c 17-52) && echo SUCCESS generate UUID
echo 'UUID='$tempUUID'     /raid5   ext4     defaults 0 0' >> /etc/fstab && echo SUCCESS mount the RAID using UUID
mount -a && echo SUCCESS execute mount command
mdadm --detail --scan --verbose >>  /etc/mdadm.conf && echo SUCCESS save the raid configuration


# set up LVM for the RAID
pvcreate /dev/sd[b-d]1 && echo SUCCESS physical volume  create
vgcreate vg1 /dev/sd[b-d]1 && echo SUCCESS volume group create
lvcreate -n lvr5 --type raid5 -l 100%FREE -i 2 vg1  && echo SUCCESS logical volume create


# create xfs on top of it
mkfs.xfs /dev/vg1/lvr5 && echo SUCCESS format xfs


# mount it to any folder;
mkdir /mnt/lvr5 && echo SUCCESS mkdir for raid mount
mount -t ext4 /dev/vg1/lvr5 /mnt/lvr5 && echo SUCCESS mount for raid


# explode the folder into the network with NFS
yum install nfs-utils nfs-utils-lib -y  && echo SUCCESS install nfs
sudo systemctl enable rpcbind
sudo systemctl enable nfs-server
sudo  systemctl enable nfs-lock
sudo systemctl enable nfs-idmap
sudo systemctl start rpcbind
sudo systemctl start nfs-server
sudo systemctl start nfs-lock
sudo systemctl start nfs-idmap
echo '/mnt/lvr5 192.168.10.0/24(rw,sync,no_root_squash,no_all_squash)' >> /etc/exports
systemctl restart nfs-server
