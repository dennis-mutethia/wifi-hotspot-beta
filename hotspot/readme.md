
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
Login By #Chack ONLY HTTP PAP
DNS Servers = `208.67.222.123` and `208.67.220.123` - Family Shield (To block Adult Content)
```
5. Go to `IP > Hotspot > Users` and create a new user 
```
server = server1
name = DFRSCGS #or your preferred username
password = TgdV&^84 #or your preferred password
```
6. Go to `IP > Hotspot > User Profiles` and update
```
Shared Users = 254
```
7. Go to `IP > Hotspot > Walled Garden` and add
```
https://hotspot-seven.vercel.app
https://youtube.com
```
