import basic
from pythonping import ping as pping


def ping(host, cnt, tmot): #writen by AI
    try:
        responses = pping(host, count=cnt, timeout=tmot)

        for response in responses:
            if response.success:
                return True
        
        return False

    except Exception as exc:
        #print(f"DEBUG: {exc}")
        return False

try:
    servers = (basic.json_read("data"))
except(FileNotFoundError):
    servers = []
    print("No save data found, making new save data.")

while True:

    #basic.clear


    try:
        iput = int(input("1: Ping server\n2: Calculate # of items into stacks\n3: Calculate # of stacks to items\n"))

        basic.clear()

        if iput == 1: #ping
            basic.print_list(servers)
            
            iput1 = str(input("Server to ping?\nType a number for your saved servers or type a web address.\n"))

            try:
                iput = int(iput1)
                iput = str(servers[iput])
                print(f"Pinging {iput}.")
            except(ValueError):
                iput = str(iput1)


            if not iput in servers:
                servers.insert(0,iput)
                if len(servers) > 10:
                    servers.remove(servers[10])
            else:
                servers.remove(iput)
                servers.insert(0,iput)

            basic.json_write("data",servers,0)

            if ping(iput,4,2) == True:
                print("Your server is online!")
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
    
    except(ValueError): #fix bad input
        print("Oops, thats not a valid choice, try again.")