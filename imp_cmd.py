sudo apt-get update && upgrade
 
vcgencmd measure_temp # check the temperature

auto lo
iface lo inet loopback

auto eth0 
allow-hotplug eth0
iface eth0 inet manual

auto wlan0 
allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_suplicant.conf
iface default inet dhcp

auto wlan1 
allow-hotplug wlan1
iface wlan1 inet manual
wpa-roam /etc/wpa_supplicant/wpa_suplicant.conf

network={
    ssid="eduroam"
    identity="eexwa18@nottingham.ac.uk"
    password="P456Pakistan!!"
    epa=TTLS
    phase2="auth=MSCHAPV2"
    pairwisw=CCMP
    key_mgmt=WPA-PSK
}


phrase for ssh public key
waqaswaqas


Testing 123
