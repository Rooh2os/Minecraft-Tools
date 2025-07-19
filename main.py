import basic,requests,base64
from pythonping import ping as pping


def ping(host, cnt, tmot): #writen by AI
    try:
        responses = pping(host, count=cnt, timeout=tmot)

        for response in responses:
            if response.success:
                return True
        
        return False

    except Exception as exc:
        
        if settings["Debug mode"] == True:
           print(f"DEBUG: {exc}")
    return False

def get_data(host:str,*,debug:bool = False): #contact mcsrvstat api
    response = (requests.get(f"https://api.mcsrvstat.us/3/{host}"))
    outputs = basic.json.loads(response.text)
    

    if debug == True:
        print(f"DEBUG: {response.status_code}")
        print("")
        print(f"DEBUG: {outputs["online"]}")
        print("")
        print(f"DEBUG: {response.text}")
    return(outputs)


try: #get/make saved server data
    servers = (basic.json_read("data"))
except(FileNotFoundError):
    servers = []
    print("No save data found, making new save data.")

try: #get/make settings data
    settings = (basic.json_read("settings.json"))
    if settings["Debug mode"] == True:
        print(f"DEBUG: {settings}")
except(FileNotFoundError):
    settings = {
        "Open server icon": True,
        "Use advanced ping": True,
        "Max saved servers": 10,
        
        "Debug mode": False
    }
    basic.json_write("settings.json",settings,4)
    print("No settings found, making new settings.")


while True:


    try:
        iput = int(input("1: Ping server\n2: Calculate # of items into stacks\n3: Calculate # of stacks to items\n"))

        basic.clear()

        if iput == 1: #ping
            basic.print_list(servers)
            
            iput1 = str(input("Server to ping?\nType a number for your saved servers or type a web address.\n"))

            try: #is iput a number or a url
                iput = int(iput1)
                iput = str(servers[iput])
                print(f"Pinging {iput}.")
            except(ValueError):
                iput = str(iput1)


            if not iput in servers: #adds iput to saved servers if not in saved servers
                servers.insert(0,iput)
                if len(servers) > settings["Max saved servers"]:
                    servers.remove(servers[settings["Max saved servers"]])
            else: #if it is move it to top
                servers.remove(iput)
                servers.insert(0,iput)

            basic.json_write("data",servers,0)

            if settings["Use advanced ping"] == False: #only pings the server
                if ping(iput,4,2) == True:
                    print("Your server is online!")
                else:
                    print("Your server is offline.")
            else: #use the minecraft ping protocall
                data = (get_data(iput,debug=settings["Debug mode"]))

                if data["online"] == True:
                    print("Your server is online!")

                    print("Version:",data["version"])
                    
                    print("Motd:")
                    basic.print_list(data["motd"]["clean"],numbers=False)
                    
                    print(f"Player count: {data["players"]["online"]}/{data["players"]["max"]}")
                    if "list" in data["players"]:
                        print("Players:")
                        for pname in data["players"]["list"]:
                            print(pname["name"])
                    
                    if "plugins" in data:
                        print("Plugins:")
                        for plname in data["plugins"]:
                            print(plname["name"])
                    
                    if "mods" in data:
                        print("Mods:")
                        for mname in data["mods"]:
                            print(mname["name"],mname["version"])

                    if "info" in data:
                        print("Info:")
                        basic.print_list(data["info"]["clean"],numbers=False)
                    
                    if "icon" in data:
                        imgdata = str(data["icon"])
                        imgdata = str(imgdata.split(",")[1])
                        with open("icon.png","bw") as f:
                            f.write(base64.b64decode(imgdata))
                        print("The server icon has been saved as icon.png")
                        if settings["Open server icon"] == True:
                            basic.os.startfile("icon.png")
                            
                else:
                    print("Your server is offline.")

        elif iput == 2: #>Stacks
            iput = int(input("# of items?\n"))
            print(f"Stacks: {(iput//64)} Items: {iput%64}")
        
        elif iput == 3: #stacks>items
            iput = input("# of stacks\n")
            iput1 = input("# of items\n")
            print(f"You have {iput*64+iput1} items")
        
        else: #bad input
            raise(ValueError)
    
    except(ValueError,IndexError): #fix bad input
        print("Oops, thats not a valid choice, try again.")