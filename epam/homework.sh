#!/bin/bash


slog=/home/homework/homework/epam/homework.log
function main
{
clear
function config_network {
# Configuring Network Interface for DHCP
sed -i 's/ONBOOT=no/ONBOOT=yes/' /etc/sysconfig/network-scripts/ifcfg-enp0s? && echo SUCCESS change ONBOOT=no to yes
systemctl restart NetworkManager.service && echo SUCCESS network restart
echo =================================================================================
}

function config_ssh {
# SSH
yum -y install openssh-server openssh-clients && echo SUCCESS install openssh
chkconfig sshd on && echo SUCCESS sshd on
service sshd start && echo SUCCESS sshd start
# restrict ssh connections for root user and to single ssh port(iptables);
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && echo SUCCESS change PermitRootLogin to no
service sshd restart && echo SUCCESS sshd restart
iptables -A INPUT -p tcp --dport 22 -j ACCEPT && echo SUCCESS single ssh port
echo =================================================================================
}

function config_local_repo {
# add local DVD ISO as an repo(all internet repos need to be removed);
while true
do
echo 'Input path to iso(/example/)'
read pathISO
if [[ $pathISO != /*/ ]]
then
echo 'Incorrect path to iso. Please input /example/ type.'
elif [ "$?" = "0" ] | ls $pathISO ; then
break
else
echo 'Incorrect path to iso'
fi
done
echo -e 'Do you need to download iso? (1/2)
1. Yes
2. No'
read tempOption
if [[ $tempOption = 1 ]]
then
wget -P $pathISO http://mirror.datacenter.by/pub/CentOS/7.9.2009/isos/x86_64/CentOS-7-x86_64-DVD-2009.iso && echo SUCCESS download iso
nameISO=CentOS-7-x86_64-DVD-2009.iso
elif [[ $tempOption = 2 ]]
then
while true
do
echo 'Input iso name'
read nameISO
if [[ $nameISO != *.iso ]]; then
echo 'Incorrect name iso. Please input *.iso file'
elif [ "$?" = "0" ] | ls $pathISO$nameISO; then
break
else
echo 'Incorrect name iso'
fi
done
fi
yum -y install wget && echo SUCCESS install wget
mkdir /cdrom && echo SUCCESS mkdir
mount -o loop $pathISO$nameISO /cdrom
echo ''$pathISO$nameISO' /cdrom iso9660 loop 0 0' >> /etc/fstab && echo SUCCESS mount the RAID using UUID
mount -a && echo SUCCESS automount
rm -f /etc/yum.repos.d/*.repo && echo SUCCESS remove all repos
echo -e '[LocalRepo]
name=Local Repository
baseurl=file:///cdrom
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7' > /etc/yum.repos.d/local.repo && echo SUCCESS created local.repo
yum clean all && echo SUCCESS yum clean
echo =================================================================================
}

function config_raid {
# set up RAID5 on 3 more drives(the size is not matter);
input_data
yum install mdadm -y && echo SUCCESS install mdamd
for u in "${MY_ARRAY[@]}"
do
(echo n; echo p; echo 1; echo ; echo ; echo t; echo fd; echo w) | fdisk /dev/$u  && echo SUCCESS fdisk
tempPath="$tempPath /dev/"$u"1 "
done

mdadm --create /dev/md5 --level=5 --raid-devices=${#MY_ARRAY[*]} $tempPath && echo SUCCESS create md device
mdadm --detail --scan --verbose >>  /etc/mdadm.conf && echo SUCCESS save the raid configuration

# set up LVM for the RAID
pvcreate /dev/md5 && echo SUCCESS physical volume  create
vgcreate vg1 /dev/md5 && echo SUCCESS volume group create
lvcreate -n lvr5 -l 100%FREE vg1  && echo SUCCESS logical volume create

# create xfs on top of it
mkfs.xfs /dev/vg1/lvr5 && echo SUCCESS format xfs
echo y

# mount it to any folder;
mkdir $mountPoint && echo SUCCESS mkdir for raid mount
tempUUID=$(blkid /dev/vg1/lvr5 | cut -c 22-57) && echo SUCCESS generate UUID
echo 'UUID='$tempUUID'     '$mountPoint'   xfs     defaults 0 0' >> /etc/fstab && echo SUCCESS mount the RAID using UUID
mount -a  && echo SUCCESS automount
lsblk
echo =================================================================================
}

function config_nfs {
# explode the folder into the network with NFS
echo -e 'Please input mount point'
read mountPoint
echo 'SUCCESS'
yum install nfs-utils nfs-utils-lib -y  && echo SUCCESS install nfs
systemctl enable rpcbind
systemctl enable nfs-server
systemctl enable nfs-lock
systemctl enable nfs-idmap
systemctl start rpcbind
systemctl start nfs-server
systemctl start nfs-lock
systemctl start nfs-idmap
echo ''$mountPoint' 192.168.10.0/24(rw,sync,no_root_squash,no_all_squash)' >> /etc/exports
systemctl restart nfs-server  && echo SUCCESS configurating nfs-server
firewall-cmd --permanent --zone=public --add-service=nfs
firewall-cmd --permanent --zone=public --add-service=mountd
firewall-cmd --permanent --zone=public --add-service=rpc-bind
firewall-cmd --reload  && echo SUCCESS configurating firewall-cmd
echo =================================================================================
}
# mount -t nfs 192.168.10.0:/mnt/lvr5/ /mnt/nfs/

function input_data {
lsblk
echo =================================================================================
echo -e 'Please input 3-12 drives(type stop when youre done)'
tempPath=''
for i in {1..12}
do
read variable
if [ $variable = 'stop' ]
then
if [ ${#MY_ARRAY[*]} -lt 3 ]
then
echo 'You need 3 more drives'
else
break
fi
elif [[ $variable != sd? ]]
then
echo 'Incorrect drive name. Please input sd? type'
else
MY_ARRAY[i]=$variable
fi
done
echo 'SUCCESS'
echo -e 'Please input mount point'
read mountPoint
echo 'SUCCESS'
return MY_ARRAY
return mountPoint
}

function rollback_raid {
input_data
umount $mountPoint  && echo SUCCESS unmount
tempUUID=$(blkid /dev/vg1/lvr5 | cut -c 22-57)  && echo SUCCESS UUID taken
sed -i '/UUID='$tempUUID'/d' /etc/fstab  && echo SUCCESS delete from /etc/fstab
lvremove /dev/vg1/lvr5 -y  && echo SUCCESS lvremove
vgremove /dev/vg1 -y  && echo SUCCESS vgremove
pvremove /dev/md5 -y  && echo SUCCESS pvremove
rm /etc/mdadm.conf -f  && echo SUCCESS rm mdadm.conf
mdadm -S /dev/md5  && echo SUCCESS stop mdadm

for u in "${MY_ARRAY[@]}"
do
mdadm --zero-superblock /dev/"$u"1  && echo SUCCESS delete zero-superblock
(echo d; echo w;) | fdisk /dev/$u
done
lsblk
}


while true;
do
echo -e 'Hello! 

Choose what you want to do:
=================================================================================
1. Configuring Network Interface for DHCP
2. Configuring SHH (restrict ssh connections for root user and to single ssh port)
3. Add local DVD ISO as an repo(all internet repos removed)
4. Set up RAID5 on 3 more drives + LVM + xfs + mount 
5. Rollback RAID5
6. Explode the folder into the network with NFS
7. exit'

read tempOption
if [[ $tempOption = 1 ]]
then
clear
config_network
elif [[ $tempOption = 2 ]]
then
clear
config_ssh
elif [[ $tempOption = 3 ]]
then
clear
config_local_repo
elif [[ $tempOption = 4 ]]
then
clear
config_raid
elif [[ $tempOption = 5 ]]
then
clear
rollback_raid
elif [[ $tempOption = 6 ]]
then
clear
config_nfs
elif [[ $tempOption = 7 ]]
then
clear
echo 'Have a nice day!'
break
else
clear
echo -e 'Incorrect parameter. Please try again.\n================================================================================='
fi
done
}

main 2>&1 | tee -a $slog
