#!/bin/bash

if [[ "${1}" == "install" ]]; then
    echo "Complete reinstall of pack"
    cp -rf /vagrant/* /home/vagrant/splunk/
    st2 pack install file:///home/vagrant/splunk --force
    st2ctl reload --register-configs

else
    echo "Copy actions to stackstorm"
    cp -rf /vagrant/actions/* /opt/stackstorm/packs/splunk/actions/
fi
