# ii-ddc

python script to control brightness and contrast

# requirements


```
# load i2c kernel module and get priveliges
sudo modprobe i2c-dev
sudo usermod -aG i2c $USER
```

```
# install ddcutil for probing and detection
sudo apt-get install ddcutil
```

```
# install ddcci driver for character device support
sudo apt-get install dkms

git clone git@gitlab.com:ddcci-driver-linux/ddcci-driver-linux.git
cd ddcci-driver-linux
sudo make -f Makefile.dkms install
```


```
# create systemd service to force detection of ddcci devices even if they aren't detectable by driver
/etc/systemd/system/ddcci@.service

[Unit]
Description=ddcci handler
After=graphical.target
Before=shutdown.target
Conflicts=shutdown.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'echo Trying to attach ddcci to %i && success=0 && i=0 && id=$(echo %i | cut -d "-" -f 2) && while ((success < 1)) && ((i++ < 5)); do /usr/bin/ddcutil getvcp 10 -b $id && { success=1 && echo ddcci 0x37 > /sys/bus/i2c/devices/%i/new_device && echo "ddcci attached to %i"; } || sleep 5; done'
Restart=no

# add udev rules for systemd service
sudo vim /etc/udev/rules.d/99-ddcci.rules

SUBSYSTEM=="i2c-dev", ACTION=="add",\
	ATTR{name}=="NVIDIA i2c adapter*",\
	TAG+="ddcci",\
	TAG+="systemd",\
	ENV{SYSTEMD_WANTS}+="ddcci@$kernel.service"

reboot
```

```
# set privileges for non-root working of python script
sudo chown -R root:i2c /dev/bus/ddcci
sudo chmod 660 /dev/bus/ddcci/*/display
```