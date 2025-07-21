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
    
def print_list(lst:list,starting_value:str = "",print_numbers:bool = True,):
    ptr = 0
    while ptr < len(lst):
        if print_numbers == True:
            print(f"{starting_value}{ptr}: {lst[ptr]}")
        else:
            print(f"{starting_value}{lst[ptr]}")
        ptr += 1