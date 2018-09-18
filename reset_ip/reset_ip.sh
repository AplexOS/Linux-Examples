#!/bin/sh


passwd root <<EOF
root
root
EOF
cp /etc/network/interfaces_bak /etc/network/interfaces -rf
/etc/init.d/S40network restart
rm /etc/ssh/ssh_host*
sync

/etc/init.d/S50sshd restart
