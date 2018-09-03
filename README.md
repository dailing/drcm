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

# Widget
I've separated the header from normal widgets.
So the pm directly receive signals form header defined in pmClass

In case some widget don't want a head. Just define `no_head=True` as an attribute of that widget.

In case some widget want to use its own costumed icon and event. Just define `customed_header=Qlable()` 
as an attribute of that widget.

In this way, all widget can share a common set of icons(back, save, time, network, etc.). 
While some specialized icon can also be set. The best is it separate the widget from header
completely.   


RULES in design widget:
* All communication done by QSignal.
* Never call any function in pageManager. 
* RUN everything from root dir.