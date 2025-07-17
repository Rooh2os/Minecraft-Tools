import basic
from pythonping import ping as pping


def ping(host,cnt,tmot):
    try:
        pping(host,cnt,tmot)
        return True
    except Exception as exc:
        print(f"DEBUG: {exc}")
        return False


while True:

    basic.clear

    try:
        iput = int(input("1: Ping server\n2: Calculate # of items into stacks\n3: Calculate # of stacks to items\n"))

        if iput == 1: #ping
            if ping(input("Server to ping?\n"),4,2) == True:
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

    except Exception as exc: #fix bad input
        print(f"DEBUG: {exc}")
        print("Oops, thats not a valid choice, try again.")