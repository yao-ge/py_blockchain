#########################################################################
# File Name: run_user.sh
# Created Time: 2019年10月25日 星期五 23时52分24秒
#########################################################################
#!/bin/bash


device_count=$1

for (( i = 1; i <= device_count; i++));
do
	nohup sudo mate-terminal -t user$i -x /bin/sh -c "python start_device.py -m user -p 123$i" &
done

