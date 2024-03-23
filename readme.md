# ii-ddc

Script for manipulation of monitor properties via **DDC/CI**

Based on this article: https://toxblh.com/linux-upravliaiem-iarkostiu-monitora-s-poddierzhkoi-ddc-protokola/

**NOTE:** Currently supports detection of only NVIDIA cards. Anything else not tested.

## Usage

```
usage: ii-ddc.py [-h] [-s] [-b SETB] [-c SETC]

options:
  -h, --help             show this help message and exit
  -s, --show             show current values
  -b, --brightness SETB  set current brightness value
  -c, --contrast SETC    set current contrast value
```

## Prerequisites

Everything described below can be achived by running `sudo ./ii-ddc-init` and `sudo ./ii-ddc-init-post-reboot`

1. Load [`i2c-dev`](https://wiki.archlinux.org/title/I2C) kernel module. For i2c device files support to interact with i2c buses.

    ```
    sudo modprobe i2c-dev
    ```

2. Install and load [`ddcci`](https://gitlab.com/ddcci-driver-linux/ddcci-driver-linux) kernel module. For ddcci character devices support that works like a bridge-interface for i2c buses used by DDC/CI.

    ```
    sudo apt-get install dkms

    git clone https://gitlab.com/ddcci-driver-linux/ddcci-driver-linux.git
    cd ddcci-driver-linux
    sudo make -f Makefile.dkms install
    ```
3. Install [`ddcutil`](https://github.com/rockowitz/ddcutil). For forced creation of ddcci character devices via systemd service. Because ddcci driver can fail to do so in some cases.

    ```
    sudo apt-get install ddcutil
    ```

4. Create kernel module configs. Can be copied from `./ii-ddc-fs-overlay/etc/modules-load.d/`.

- `/etc/modules-load.d/ddcci.conf`:
    
    ```
    ddcci
    ddcci-backlight
    ```

- `/etc/modules-load.d/i2c-dev.conf`:

    ```
    i2c-dev
    ```

5. Create systemd template service. It's work based on [this method of instantiating devices](https://docs.kernel.org/i2c/instantiating-devices.html#method-4-instantiate-from-user-space). Can be copied from `./ii-ddc-fs-overlay/etc/systemd/system/`.

- `/etc/systemd/system/ddcci@.service`

    ```
    [Unit]
    Description=ddcci driver service
    After=graphical.target
    Before=shutdown.target
    Conflicts=shutdown.target

    [Service]
    Type=oneshot
    ExecStart=/bin/bash -c 'echo Trying to attach ddcci to %i && success=0 && i=0 && id=$(echo %i | cut -d "-" -f 2) && while ((success < 1)) && ((i++ < 5)); do /usr/bin/ddcutil getvcp 10 -b $id && { success=1 && echo ddcci 0x37 > /sys/bus/i2c/devices/%i/new_device && echo "ddcci attached to %i"; } || sleep 5; done'
    Restart=no
    ```

6. Create udev rules. For instantiation of systemd templates. Can be copied from `./ii-ddc-fs-overlay/etc/udev/rules.d/`.

- `/etc/udev/rules.d/99-ddcci.rules`

    ```
    SUBSYSTEM=="i2c", ACTION=="add",\
        ATTR{name}=="NVIDIA i2c adapter*",\
        TAG+="ddcci",\
        TAG+="systemd",\
        ENV{SYSTEMD_WANTS}+="ddcci@$kernel.service"
    ```

7. Reboot system to create new device nodes.

8. Get privileges of i2c group. And give this group ownership of new devices.

    ```
    sudo usermod -aG i2c $USER
    sudo chown -R root:i2c /dev/bus/ddcci
    sudo chmod 660 /dev/bus/ddcci/*/display
    ```

9. Create convinient symlink to shell script. (optional)

    ```
    ln -s `realpath ./ii-ddc` /usr/bin/ii-ddc
    ```