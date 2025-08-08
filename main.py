import basic,requests,base64,zipfile
from PIL import Image
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
    settings = (basic.json_read("config.txt"))
    if settings["Debug mode"] == True:
        print(f"DEBUG: {settings}")
except(FileNotFoundError):
    settings = {
        "Open server icon": True,
        "Save individual icons": False,
        "Use advanced ping": True,
        "Max saved servers": 10,
        "Starting value for lists": "    ",
        
        "Debug mode": False
    }
    basic.json_write("config.txt",settings,4)
    print("No settings found, making new settings.")

#try: #make pack folder
#    basic.os.mkdir("packs")
#    print("No packs folder found. Making packs folder")
#except(FileExistsError):
#    pass

while True:


    try:
        iput = int(input("1: Ping server\n2: Make a template resorce pack\n3: Calculate # of items into stacks\n4: Calculate # of stacks to items\n"))

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
                    basic.print_list(data["motd"]["clean"],settings["Starting value for lists"],print_numbers=False)
                    
                    print(f"Player count: {data["players"]["online"]}/{data["players"]["max"]}")
                    if "list" in data["players"]:
                        print("Players:")
                        for pname in data["players"]["list"]:
                            print(settings["Starting value for lists"] + pname["name"])
                    
                    if "plugins" in data:
                        print("Plugins:")
                        for plname in data["plugins"]:
                            print(settings["Starting value for lists"] + plname["name"])
                    
                    if "mods" in data:
                        print("Mods:")
                        for mname in data["mods"]:
                            print(settings["Starting value for lists"] + mname["name"],mname["version"])

                    if "info" in data:
                        print("Info:")
                        basic.print_list(data["info"]["clean"],settings["Starting value for lists"],print_numbers=False)
                    
                    if "icon" in data:
                        imgdata = str(data["icon"])
                        imgdata = str(imgdata.split(",")[1])

                        if settings["Save individual icons"]:
                            try:
                                basic.os.mkdir("icons")
                            except(FileExistsError):
                                pass
                            with open(f"icons/{iput}.png","wb") as f:
                                f.write(base64.b64decode(imgdata))
                            
                            print(f"The server icon has been saved as {iput}.png")
                            if settings["Open server icon"] == True:
                                icon = Image.open(f"icons/{iput}.png")
                                icon.show()
                                #basic.os.startfile(f"icons/{iput}.png")
                        else:
                            with open("icon.png","wb") as f:
                                f.write(base64.b64decode(imgdata))
                        
                            print("The server icon has been saved as icon.png")
                            if settings["Open server icon"] == True:
                                icon = Image.open("icon.png")
                                icon.show()
                                #basic.os.startfile("icon.png")
                            
                else:
                    print("Your server is offline.")

        elif iput == 2: #make pack
            iput = input("Version name?\n")

            data = (requests.get("https://piston-meta.mojang.com/mc/game/version_manifest.json"))

            if settings["Debug mode"] == True:
                print(data.json())

            data = (data.json())

            if settings["Debug mode"] == True:
                print(data)
            data = data["versions"]
            
            iput1 = int(0)
            for v in data:
                if v["id"] == iput:
                    break
                if settings["Debug mode"]:
                    print(v["id"])
                iput1 += 1

            if settings["Debug mode"]:
                print(iput1)

            if settings["Debug mode"]:
                print(len(data))
            if iput1+1 > (len(data)):
                print("Could not find your version. Check the spelling.")
                raise(ValueError)
            
            #data = (requests.get(requests.get(data[iput1]["url"])["downloads"]["client"]["url"]))
            data = requests.get(data[iput1]["url"])
            data = requests.get(data.json()["downloads"]["client"]["url"])

            if settings["Debug mode"] == True:
                print(data.text)

            with open("temp","wb") as f:
                f.write(data.content)


            with zipfile.ZipFile("temp","r") as zip:
                if settings["Debug mode"]:
                    print(zip.namelist())
                zip.extract("version.json",".")
                basic.os.rename("version.json","temp1")
                for file in zip.namelist():
                    if file.startswith("assets/"):
                        zip.extract(file,f"./packs/{iput}")

            mcmeta = (basic.json_read("temp1"))
            
            try:
                mcmeta = {
                    "pack":{
                        "description": "Made with Minecraft Tools by Rooh2os",
                        "pack_format": (mcmeta["pack_version"]["data"])
                    }
                }
            except(TypeError):
                mcmeta = {
                    "pack":{
                        "description": "Made with Minecraft Tools by Rooh2os",
                        "pack_format": (mcmeta["pack_version"])
                    }
                }
            
            basic.json_write(f"packs/{iput}/pack.mcmeta",mcmeta,4)

            basic.os.remove("temp")
            basic.os.remove("temp1")

            print(f"Template pack for {iput} made sucessfully")

        elif iput == 3: #>Stacks
            iput = int(input("# of items?\n"))
            print(f"Stacks: {(iput//64)} Items: {iput%64}")
        
        elif iput == 4: #stacks>items
            iput = int(input("# of stacks\n"))
            iput1 = int(input("# of items\n"))
            print(f"You have {iput1 + iput * 64} items")
        
        
        else: #bad input
            raise(ValueError)
    
    except(KeyError):
        basic.os.remove("temp")
        print("You must use a version above 1.14")

    except(ValueError,IndexError): #fix bad input
        print("Oops, thats not a valid choice, try again.")