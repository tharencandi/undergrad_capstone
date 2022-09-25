MOUNTPOINT="/home/haeata/.glibiostoma_data"
DEVICE="/dev/$(lsblk -fs | grep -e "ntfs" | grep -e "Passport" | cut -f1 -d" ")"

if [[ -e $MOUNTPOINT  && -d $MOUNTPOINT ]]; then
	echo $MOUNTPOINT exists
else
	echo $MOUNTPOINT does not exist
	echo Creating directory $MOUNTPOINT
	mkdir $MOUNTPOINT
fi

echo "Device: $DEVICE, Mountpoint: $MOUNTPOINT"
echo -n "Proceed [y/n]: "
read -r CONFIRM

if [[ $CONFIRM == "y" ]]; then
	echo "Mounting device..."
	sudo mount -t ntfs3 $DEVICE $MOUNTPOINT
else
	echo "aborting..."
	exit 1
fi

