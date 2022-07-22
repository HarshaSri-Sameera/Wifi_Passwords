import subprocess
import re

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()     
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))        # finds all the user profiles
wifi_list = []
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):       # allows only the security key : "present" ones
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)        # searches for the key content 
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile)   # appending every entry into a list

for x in range(len(wifi_list)):  # printing the list
    print(wifi_list[x])
