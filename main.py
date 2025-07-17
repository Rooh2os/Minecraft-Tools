import basic,math
from pythonping import ping as pping


def ping(host,cnt,tmot):
    try:
        pping(host,cnt,tmot)
        return True
    except Exception as exc:
        print(f"DEBUG: {exc}")
        return False

while True:
    try:
        input = int(input("1: Ping server\n2: Calculate # of items into stacks\n3: Calculate # of stacks to items\n"))

        if input == 1: #ping
            if ping(input("Server to ping?\n"),4,2) == True:
                print("Your server is online!")
            else:
                print("Your server is offline.")
        elif input == 2: # #>Stacks
            input = input("# of items?")
            print(f"Stacks: {math.floor(input/64)} Items: {input%64}")
    except(ValueError):
        print("Oops, thats not a valid choice, try again.")