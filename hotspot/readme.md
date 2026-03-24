
## Mikrotik Router Setup Guide
1. Download <a href="https://mikrotik.com/download">Winbox</a>
2. Reset Your Mikrotik AP or Create a new WiFi and give it a name e.g `MatrixSys Free WiFi`
- - This can be acieved by going to `Quick Set` and Select `Wisp AP`
```
Configuration Mode = Router
Internet = Automatic/Dynamic
Local IP = 192.168.88.1
```
3. Go to `IP > Hotspot` and create a new Hotspot
4. Go to `IP > Hotspot > Server Profiles` update 
```
hotspot address = 192.168.88.1
DNS Name = hotspot.matrixsys.wifi #Or your preferred name
Login By #Check ONLY HTTP PAP
DNS Servers = `208.67.220.123` and `208.67.222.123` - Family Shield (To block Adult Content)
```
5. Create 250 users
```
:local i 1
:while ($i <= 250) do={ 
/ip hotspot user add name="user-$i" password="TgdV84" 
:set $i ($i + 1) 
}
```
6. Go to `IP > Hotspot > User Profiles` and update
```
Shared Users = 254
Rate Limit (rx/tx) = 1M/1M
```
7. Add Walled Garden for Backend & Media Access (allows access without login). Open Terminal and
```
#Backend
/ip hotspot walled-garden 
add action=allow dst-host=matrix-hotspot.vercel.app
add action=allow dst-host=i.postimg.cc

#Youtube
/ip hotspot walled-garden
add action=allow dst-host=*.youtube.com
add action=allow dst-host=*.googlevideo.com
add action=allow dst-host=*.ytimg.com
add action=allow dst-host=*.ggpht.com
add action=allow dst-host=*.gstatic.com
add action=allow dst-host=*.googleapis.com
add action=allow dst-host=*.google.com
add action=allow dst-host=youtube.com
add action=allow dst-host=googlevideo.com
add action=allow dst-host=ytimg.com

#Google
/ip hotspot walled-garden ip
add action=accept dst-address=8.8.8.8 comment="Google DNS"
add action=accept dst-address=8.8.4.4 comment="Google DNS"

#Captive portal
/ip hotspot walled-garden
add action=allow dst-host=connectivitycheck.gstatic.com
add action=allow dst-host=connectivitycheck.android.com
add action=allow dst-host=captive.apple.com
add action=allow dst-host=www.apple.com
add action=allow dst-host=www.msftconnecttest.com
add action=allow dst-host=detectportal.firefox.com
add action=allow dst-host=*.gstatic.com
```
8. Enable hotspot & scheduler
```
system device-mode
print
update scheduler=yes hotspot=yes
```
9. Schedule Hourly Reboot
```
/system scheduler add name=hourly-reboot start-time=00:00:00 interval=1h on-event="/system reboot"
```
10. Go to `IP > DHCP Server`
```
Double click the DHCP SERVER and update
Check Always Broadcast
Check Add ARP for Leases
```