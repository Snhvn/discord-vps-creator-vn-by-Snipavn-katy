wget -O- --no-check-certificate http://drive.muavps.net/windows/Windows2012r2.gz | gunzip | dd of=2012r2.img && 
qemu-system-x86_64 \
-net nic -net user,id=n0,hostfwd=tcp::3389-:3389 \
-m 2G -smp cores=2 \
-cpu max \
-boot order=d \
-drive file=2012r2.img,format=raw,if=virtio \
-device usb-ehci,id=usb,bus=pci.0,addr=0x4 \
-device usb-tablet \
-vnc :0 -vga virtio \
-device virtio-gpu \
&>/dev/null &
