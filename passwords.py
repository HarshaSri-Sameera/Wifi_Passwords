import subprocess
import re
command_output = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
profile_names = (re.findall("All User Profiles    : (.*)\r", command_output))
wifi_list = []
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(
            ["netsh", "wlan", "show", "profiles", name], capture_output=True)
        if re.search("security key          : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(
                ["netsh", "wlan", "show", "profiles", name, "key=clear"], capture_output=True).stdout.decode()
            password = re.search("key content    : (.*)\r", profile_info_pass)
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]

        wifi_list.append(wifi_profile)
        print("done running!")

    for x in range(len(wifi_list)):
        print(wifi_list[x])
