# xddc

Script for manipulation of monitor properties via **DDC/CI**

## usage

```
usage: xddc.py [-h] [-s] [-b SETB] [-c SETC]

options:
  -h, --help             show this help message and exit
  -s, --show             show current values
  -b, --brightness SETB  set current brightness value
  -c, --contrast SETC    set current contrast value
```

## prerequisites

Everything described below can be achived by running `sudo ./install`

1. Load [`i2c-dev`](https://wiki.archlinux.org/title/I2C) kernel module and add current user to `i2c` group. For i2c device files support to interact with i2c buses.

    ```
    sudo modprobe i2c-dev
    usermod -aG i2c $USER
    ```

2. Install and load [`ddcci`](https://gitlab.com/ddcci-driver-linux/ddcci-driver-linux) kernel module. For ddcci character devices support that works like a bridge-interface for i2c buses used by DDC/CI (much faster interface than `ddcutil`)

    ```
    sudo apt-get install dkms

    git clone https://gitlab.com/ddcci-driver-linux/ddcci-driver-linux.git
    cd ddcci-driver-linux
    sudo make -f Makefile.dkms install
    sudo modprobe ddcci
    ```
3. Install [`ddcutil`](https://github.com/rockowitz/ddcutil). For smart creation of ddcci character devices. Because ddcci driver can fail to do so in some cases.

    ```
    sudo apt-get install ddcutil
    ```

4. Install [kernel modules config](xddc-fs-overlay/etc/modules-load.d/xddc.conf) to `/etc/modules-load.d/`.

5. Install [configuration script](xddc-fs-overlay/usr/local/bin/xddc-configure) to `/usr/local/bin/xddc-configure` (path required by `xddc-configure.service` next step).

6. Install [systemd service](xddc-fs-overlay/usr/local/lib/systemd/system/xddc-configure.service) to one of `/systemd/system/` directories.

7. Install [xddc.py](xddc-fs-overlay/usr/local/bin/xddc.py) and [xddc](xddc-fs-overlay/usr/local/bin/xddc) to one of `/bin/` directories for convinience.

8. Reload systemd daemon and enable `xddc-configure.service`

    ```
    sudo systemctl daemon-reload
    sudo systemctl enable xddc-configure.service
    ```

9. Reboot.

10. Enjoy :)

## references

[Article on which this was project based](https://toxblh.com/linux-upravliaiem-iarkostiu-monitora-s-poddierzhkoi-ddc-protokola/)\
[VESA DDC/CI Standard](https://glenwing.github.io/docs/VESA-DDCCI-1.1.pdf)\
[DDC/CI specifications](https://boichat.ch/nicolas/ddcci/specs.html)
