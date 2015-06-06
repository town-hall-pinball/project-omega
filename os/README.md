PinOS
=====

Stuff related to RasperryPi O/S and running the No Fear P-ROC software.

# Image

I (dagent) am leaving the image up at my [personal website](http://notsourgent.com/thp/) for now, as it's over 1GB (the uncompressed image is 3.2GB).  The OS is my hack at the official [Raspbian](http://www.raspberrypi.org/downloads/) (made from Debian Wheezy for the Pi).  Basically, I've made it read-only, installed some useful stuff, and it has *all the deps* for our project.

## Installation

(Quick and dirty for now).
* Requirements: Linux/Unix OS, Good 4GB+ SD card, the image file (called dgpi.iso below)
* Figure out what device your computer sees the SD card as (I'll call it /dev/sdcard below)
* run `bzip2 -dc dgpi.iso.bz2 | dd of=/dev/sdcard bs=512` until done
* Possibly run a partioning tool on /dev/sdcard to use the remaining space
* When done, pop it into the Pi and boot

## Use

* Network: Uses DHCP as well as 192.168.42.1
* Login: `ssh pi@192.168.42.1` with password `raspberry`
* `~/town-hall-pinball` exists -- cd to no-fear directory and run `./myrun` to get things going
* Disk is mounted read-only!  Run `mountrw` to switch to read-write, and `mountro` to switch back.
* *Do not remove power in read-write mode!!!*  It's OK to remove power in read-only mode.  If stuck in read-write, run `sudo shutdown -h now` and wait 30s before removing power.

## Links

I'll have more later.

* https://wiki.archlinux.org/index.php/disk_cloning


