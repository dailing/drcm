# drcm
DR camera

## Auto start:
Please copy the drcm.desktop file to 
```
/etc/xdg/autostart/drcm.desktop
```
If something wrong with the DISPLAY device
copy ```/home/pi/.Xauthority```
to  ```/root/.Xauthority```

The output of DRCM.py will be writen to ```/tmp/drcm.log```

If the auto start not work, check the environment variable. 
Add ```export XDG_CONFIG_DIRS=/etc/xdg``` to ```/etc/profile``` 
to solve this problem. 

#camera config
ccd:参数设置：曝光时间，屈光度，hue，白平衡
闪光灯的电阻
测闪光灯瞬时电压，
ccd安装底盘