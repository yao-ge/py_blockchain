#########################################################################
# File Name: run_node.sh
# Created Time: 2019年10月25日 星期五 23时52分24秒
#########################################################################
#!/bin/bash


device_count=$1

for (( i = 1; i <= device_count; i++));
do
	nohup sudo mate-terminal -t node$i -x /bin/sh -c "python start_device.py -m node -p 1234" &
done
