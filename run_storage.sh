#########################################################################
# File Name: run_storage.sh
# Created Time: 2019年10月25日 星期五 23时52分24秒
#########################################################################
#!/bin/bash


device_count=$1

for (( i = 1; i <= device_count; i++));
do
	nohup sudo mate-terminal -t storage$i -x /bin/sh -c "python3 start_device.py -m storage -p 323$i" >> ./logs/storage$i.log &
done

