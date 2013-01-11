#!/bin/bash
cd /mnt/data/dist/render_manager/fedora_15/
./uninstall.sh
cp /mnt/opt/cgru/afrender /etc/init.d/
chkconfig --add afrender
/etc/init.d/afrender start