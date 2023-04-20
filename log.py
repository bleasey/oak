import os
from commit import Commit
from colorama import Fore, init

# Auto reset colour scheme
init(autoreset=True)

class Log(staticmethod):

    def log(main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak"))

        # Checking if HEAD exists
        if not os.path.exists("HEAD"):
            print("No commits made")
            return
        
        with open("HEAD", 'r') as file:
            curr_hash = file.readline()
        
        # Display head in first iteration
        print(Fore.YELLOW + f"commit\t{curr_hash} (" + Fore.BLUE + "HEAD" + Fore.YELLOW + ")")
        print(f"Date:\t{Commit.get_date(curr_hash, main_dir)}")
        print(Fore.BLUE + f"\t{Commit.get_comment(curr_hash, main_dir)}")
        print()
        # curr_hash should now equal to it's parent commit hash
        curr_hash = Commit.get_parent_hash(curr_hash, main_dir)

        # Other iterations
        while(curr_hash!="NULL"):
            print(Fore.YELLOW + f"commit\t{curr_hash}")
            print(f"Date:\t{Commit.get_date(curr_hash, main_dir)}")
            print(Fore.BLUE + f"\t{Commit.get_comment(curr_hash, main_dir)}")
            print()
            # curr_hash should now equal to it's parent commit hash
            curr_hash = Commit.get_parent_hash(curr_hash, main_dir)

        os.chdir(initial_dir)
        return
    
    def short_log(main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak"))

        # Checking if HEAD exists
        if not os.path.exists("HEAD"):
            print("No commits made")
            return
        
        with open("HEAD", 'r') as file:
            curr_hash = file.readline()
        
        # Display head in first iteration
        print(Fore.YELLOW + curr_hash + "  " + Fore.BLUE + Commit.get_comment(curr_hash, main_dir) + Fore.YELLOW + " (" + Fore.BLUE + "HEAD" + Fore.YELLOW + ")")
        # curr_hash should now equal to it's parent commit hash
        curr_hash = Commit.get_parent_hash(curr_hash, main_dir)

        # Other iterations
        while(curr_hash!="NULL"):
            print(Fore.YELLOW + curr_hash + "  " + Fore.BLUE + Commit.get_comment(curr_hash, main_dir))
            # curr_hash should now equal to it's parent commit hash
            curr_hash = Commit.get_parent_hash(curr_hash, main_dir)
        
        print()
        os.chdir(initial_dir)
        return

# Class definition ends