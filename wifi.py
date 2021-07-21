class Wifi:
    @classmethod
    def getSSID(cls) -> list:
        output = __import__("subprocess").run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

        ssid = list()

        for i in output.split("\r\n"):
            i = "".join(i.split()) # delete whitespace
            
            if i.startswith("AllUserProfile"):
                
                ssid.append(i.split(":")[1])
        
        return ssid
    
    @classmethod
    def getWifiInfo(cls) -> list:
        networks = list()

        ssid = cls.getSSID()

        for s in ssid:
            output = __import__("subprocess").run(["netsh", "wlan", "show", "profile", s], capture_output=True).stdout.decode()

            for l in output.split("\r\n"):
                l = "".join(l.split()) # delete whitespace

                if l.startswith("Securitykey"):
                    if l.split(":")[1] == "Present":
                        # Present means you can get the password

                        output = __import__("subprocess").run(["netsh", "wlan", "show", "profile", s, "key=clear"], capture_output=True).stdout.decode()

                        # Get password

                        for j in output.split("\r\n"):
                            j = "".join(j.split()) # delete whitespace

                            if j.startswith("KeyContent"):
                                
                                networks.append({"ssid":s, "password": j.split(":")[1]})
        
        return networks

if __name__ == "__main__": # if script is executed directly
    import pprint

    pprint.pprint(Wifi.getSSID())

    print() # newline

    pprint.pprint(Wifi.getWifiInfo())