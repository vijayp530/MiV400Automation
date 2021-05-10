#Initialize modules to play audio via pxcon
/sbin/modprobe csx_gist
/sbin/modprobe csx_halaudio
mknod /dev/csx_gist c 239 0
