import os
from colorama import Fore, init

# Auto reset colour scheme
init(autoreset=True)

def init():
    base_dir = os.getcwd()
    # checking if .oak already exists
    if os.path.exists(os.path.join(base_dir, ".oak")):
        print(Fore.YELLOW + "Error: repository already exists")
        return
    
    # In the base directory
    # Creating .oak
    os.mkdir(".oak")
    os.chdir(".oak")

    # Adding stuff inside .oak
    os.mkdir("objects")

    print(Fore.GREEN + "Initialized empty oak repository")
    return

init()
