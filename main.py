#cspell:ignore Rooh2os imgdata mcsrvstat plname pname pping pythonping resorce startfile tmot Hypixel
import basic,requests,base64,zipfile
from PIL import Image
from pythonping import ping as pping

#define vars
config = dict
servers = list
iput = str #also sometimes an int
iput1 = str #also sometimes an int
debug = bool





def ping(host, cnt, tmot): #written by AI
    try:
        responses = pping(host, count=cnt, timeout=tmot)

        for response in responses:
            if response.success:
                return True
        
        return False

    except Exception as exc:
        
        if config["Debug mode"] == True: # type: ignore
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

try: #get/make config data
    config = (basic.json_read("config.txt"))
    if config["Debug mode"] == True:
        print(f"DEBUG: {config}")
except(FileNotFoundError):
    config = {
        "Open images": True,
        "Save individual icons": False,
        "Use advanced ping": True,
        "Max saved servers": 10,
        "Starting value for lists": "    ",
        
        "Debug mode": False
    }
    basic.json_write("config.txt",config,4)
    print("No config found, making new config.")

debug = config["Debug mode"]

try: #get/make aliases
    aliases = (basic.json_read("aliases"))
    if config["Debug mode"] == True:
        print(f"DEBUG: {config}")
except(FileNotFoundError):
    aliases = {
        "Hypixel": "mc.hypixel.net"
    }
    basic.json_write("aliases",aliases,4)
    print("No aliases found, making new aliases.")

#try: #make pack folder
#    basic.os.mkdir("packs")
#    print("No packs folder found. Making packs folder")
#except(FileExistsError):
#    pass

while True:


    try:
        iput = int(input("1: Ping a server\n2: Make a template resorce pack\n3: Get a user's skin\n4: Get a user's head\n5: Get a user's usable skin\n6: Make a server alias\n7: Calculate # of items into stacks\n8: Calculate # of stacks to items\n"))

        basic.clear()

        if iput == 1: #ping
            basic.print_list(servers)
            
            iput1 = str(input("Server to ping?\nType a number for your saved servers or type a web address.\n"))

            if iput1 in aliases:
                iput = aliases[iput1]

                if not iput1 in servers: #adds iput to saved servers if not in saved servers
                    servers.insert(0,iput1)
                    if len(servers) > config["Max saved servers"]:
                        servers.remove(servers[config["Max saved servers"]])
                else: #if it is move it to top
                    servers.remove(iput1)
                    servers.insert(0,iput1)

            else:            
                try: #is iput a number or a web address
                    iput = int(iput1)
                    iput = str(servers[iput])
                    
                    if iput in aliases:
                        servers.remove(iput)
                        servers.insert(0,iput)
                        iput = aliases[iput]
                        do_check = False


                    print(f"Pinging {iput}.")
                except(ValueError):
                    iput = str(iput1)
                    do_check = True

                if do_check:
                    if not iput in servers: #adds iput to saved servers if not in saved servers
                        servers.insert(0,iput)
                        if len(servers) > config["Max saved servers"]:
                            servers.remove(servers[config["Max saved servers"]])
                    else: #if it is move it to top
                        servers.remove(iput)
                        servers.insert(0,iput)

            basic.json_write("data",servers,0)

            if config["Use advanced ping"] == False: #only pings the server
                if ping(iput,4,2) == True:
                    print("Your server is online!")
                else:
                    print("Your server is offline.")
            else: #use the minecraft ping protocol
                data = (get_data(iput,debug=config["Debug mode"]))

                if data["online"] == True:
                    print(f"\n{config["Starting value for lists"]}Your server is online!")

                    print(f"\n{config["Starting value for lists"]}Version:",data["version"])
                    
                    print(f"\n{config["Starting value for lists"]}Motd:")
                    basic.print_list(data["motd"]["clean"],(config["Starting value for lists"] * 2),print_numbers=False)
                    
                    print(f"\n{config["Starting value for lists"]}Player count: {data["players"]["online"]}/{data["players"]["max"]}")
                    if "list" in data["players"]:
                        print("Players:")
                        for pname in data["players"]["list"]:
                            print((config["Starting value for lists"] * 2) + pname["name"])
                    
                    if "plugins" in data:
                        print(f"\n{config["Starting value for lists"]}Plugins:")
                        for plname in data["plugins"]:
                            print((config["Starting value for lists"] * 2) + plname["name"])
                    
                    if "mods" in data:
                        print(f"\n{config["Starting value for lists"]}Mods:")
                        for mname in data["mods"]:
                            print((config["Starting value for lists"] * 2) + mname["name"],mname["version"])

                    if "info" in data:
                        print(f"\n{config["Starting value for lists"]}Info:")
                        basic.print_list(data["info"]["clean"],(config["Starting value for lists"] * 2),print_numbers=False)
                    
                    if "icon" in data:
                        imgdata = str(data["icon"])
                        imgdata = str(imgdata.split(",")[1])

                        if config["Save individual icons"]:
                            try:
                                basic.os.mkdir("icons")
                            except(FileExistsError):
                                pass
                            with open(f"icons/{iput}.png","wb") as f:
                                f.write(base64.b64decode(imgdata))
                            
                            print(f"\n{config["Starting value for lists"]}The server icon has been saved as {iput}.png")
                            if config["Open images"] == True:
                                icon = Image.open(f"icons/{iput}.png")
                                icon.show()
                                #basic.os.startfile(f"icons/{iput}.png")
                        else:
                            with open("icon.png","wb") as f:
                                f.write(base64.b64decode(imgdata))
                        
                            print(f"\n{config["Starting value for lists"]}The server icon has been saved as icon.png")
                            if config["Open images"] == True:
                                icon = Image.open("icon.png")
                                icon.show()
                                #basic.os.startfile("icon.png")
                            
                else:
                    print(f"\n{config["Starting value for lists"]}Your server is offline.")

        elif iput == 2: #make pack
            iput = input("Version name?\n")

            data = (requests.get("https://piston-meta.mojang.com/mc/game/version_manifest.json"))

            if config["Debug mode"] == True:
                print(data.json())

            data = (data.json())

            if config["Debug mode"] == True:
                print(data)
            data = data["versions"]
            
            iput1 = int(0)
            for v in data:
                if v["id"] == iput:
                    break
                if config["Debug mode"]:
                    print(v["id"])
                iput1 += 1

            if config["Debug mode"]:
                print(iput1)

            if config["Debug mode"]:
                print(len(data))
            if iput1+1 > (len(data)):
                print("Could not find your version. Check the spelling.")
                raise(ValueError)
            
            #data = (requests.get(requests.get(data[iput1]["url"])["downloads"]["client"]["url"]))
            data = requests.get(data[iput1]["url"])
            data = requests.get(data.json()["downloads"]["client"]["url"])

            if config["Debug mode"] == True:
                print(data.text)

            with open("temp","wb") as f:
                f.write(data.content)


            with zipfile.ZipFile("temp","r") as zip:
                if config["Debug mode"]:
                    print(zip.namelist())
                zip.extract("version.json",".")
                basic.os.rename("version.json","temp1")
                for file in zip.namelist():
                    if file.startswith("assets/"):
                        zip.extract(file,f"./packs/{iput}")

            mcmeta = (basic.json_read("temp1"))
            
            try:
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
                            "pack_format": (mcmeta["pack_version"]["resource_major"])
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

            print(f"Template pack for {iput} made successfully")

        elif iput == 3: #get user skin
            iput = input("Username or UUID?\n")
            data = requests.get(f"https://mineskin.eu/armor/body/{iput}")
            
            if debug:
                print(data.text)
            
            try:
                basic.os.mkdir("skins")
            except(FileExistsError):
                pass

            with open(f"skins/{iput}_skin.png","wb") as image:
                image.write(data.content)
            print(f"{iput}'s skin saved successfully")

            if config["Open images"]:
                image = Image.open(f"skins/{iput}_skin.png")
                image.show()

        elif iput == 4: #get user head
            iput = input("Username or UUID?\n")
            data = requests.get(f"https://mineskin.eu/helm/{iput}")
            
            if debug:
                print(data.text)
            
            try:
                basic.os.mkdir("skins")
            except(FileExistsError):
                pass

            with open(f"skins/{iput}_head.png","wb") as image:
                image.write(data.content)
            print(f"{iput}'s head saved successfully")

            if config["Open images"]:
                image = Image.open(f"skins/{iput}_head.png")
                image.show()
        
        elif iput == 5: #get user skin for use
            iput = input("Username or UUID?\n")
            data = requests.get(f"https://mineskin.eu/skin/{iput}")
            
            if debug:
                print(data.text)
            
            try:
                basic.os.mkdir("skins")
            except(FileExistsError):
                pass

            with open(f"skins/{iput}_usable_skin.png","wb") as image:
                image.write(data.content)
            print(f"{iput}'s usable skin saved successfully")

            if config["Open images"]:
                image = Image.open(f"skins/{iput}_usable_skin.png")
                image.show()

        elif iput == 6: #make a server alias
            iput = input("Alias name?\n")
            aliases[iput] = input("Alias address?\n")

            basic.json_write("aliases",aliases,0)

        elif iput == 7: #items>Stacks
            iput = int(input("# of items?\n"))
            print(f"Stacks: {(iput//64)} Items: {iput%64}")
        
        elif iput == 8: #stacks>items
            iput = int(input("# of stacks\n"))
            iput1 = int(input("# of items\n"))
            print(f"You have {iput1 + iput * 64} items")
        
        else: #bad input
            raise(ValueError)
    
    except(KeyError):
        basic.os.remove("temp")
        basic.os.remove("temp1")
        basic.os.remove("version.json")
        print("You must use a version above 1.14")

    except(ValueError,IndexError): #fix bad input
        print("Oops, thats not a valid choice, try again.")