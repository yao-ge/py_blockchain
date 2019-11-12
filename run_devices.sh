#########################################################################
# File Name: run_devices.sh
# Created Time: 2019年10月26日 星期六 06时03分29秒
#########################################################################
#!/bin/bash

python3 init_cfg.py 

rm ./*.pcap

while getopts ":u:n:s:" opt
do
	case $opt in
		u)
			./run_user.sh $OPTARG
			;;
		n)
			./run_node.sh $OPTARG
			;;
		s)
			./run_storage.sh $OPTARG
			;;
		?)
			echo ""
			echo " this is a script for run devices"
			echo " -u           user mode, specify number of users"
			echo " -n           node mode, specify number of nodes"
			echo " -s           storage mode, specify number of storages"
			echo " -h --help    print help info"
			echo ""
			exit 1
			;;
	esac
done

