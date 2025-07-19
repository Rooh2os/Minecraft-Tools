import os,json

def clear():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

def json_write(file:str,data,indent:int):
    with open(file,"w") as f:
        json.dump(data,f,indent=indent)

def json_read(file:str):
    try:
        with open(file,"r") as f:
            return json.load(f)
    except(FileNotFoundError):
        raise(FileNotFoundError)
    
def print_list(lst:list,*,numbers:bool = True):
    ptr = 0
    while ptr < len(lst):
        if numbers == True:
            print(f"{ptr}: {lst[ptr]}")
        else:
            print(f"{lst[ptr]}")
        ptr += 1