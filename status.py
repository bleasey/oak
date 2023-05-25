import os
import hashlib
from blob import Blob
from colorama import Fore, init

# Auto reset colour scheme
init(autoreset=True)

# Class definition begins
class Status(staticmethod):
    
    # Main function to display status
    def get_status():
        index_content = []
        prev_index_content = []
        # Getting the index content
        with open(os.path.join('.oak', 'index'), 'r') as index:
            index_content = index.readlines()

        if os.path.exists(os.path.join('.oak', 'prev_index')):
            with open(os.path.join('.oak', 'prev_index'), 'r') as prev_index:
                prev_index_content = prev_index.readlines()

        # Sorting the two content files
        index_content.sort()
        prev_index_content.sort()

        # Defining lists containing names and hashes of prev_index files
        prev_index_fname = []
        prev_index_fhash = []

        # Splitting the text for each string in index_content to get name and hash
        # Removing the final character '\n' from 2nd word for elements in index_content
        for i in range(len(prev_index_content)):
            prev_index_content[i] = prev_index_content[i].split('\t')
            prev_index_fname.append(prev_index_content[i][0])
            prev_index_fhash.append(prev_index_content[i][1][:-1])

        # Defining lists containing names and hashes of index files
        index_fname = []
        index_fhash = []

        # Splitting the text for each string in index_content to get name and hash
        # Removing the final character '\n' from 2nd word for elements in index_content
        for i in range(len(index_content)):
            index_content[i] = index_content[i].split('\t')
            index_fname.append(index_content[i][0])
            index_fhash.append(index_content[i][1][:-1])


        # Defining required lists
        new_staged = []
        modified_staged = []
        deleted_staged = []
        Status.get_staged(new_staged, modified_staged, deleted_staged, index_fname, index_fhash, prev_index_fname, prev_index_fhash)

        untracked = []
        modified_unstaged = []
        deleted_unstaged = []
        Status.get_untracked(untracked, index_fname, ".", os.getcwd())
        Status.get_modified_deleted_unstaged(modified_unstaged, deleted_unstaged, index_fname, index_fhash)

        # Displaying the status details

        # Defining bool variables
        changes_to_be_committed_absent = (len(new_staged) == len(modified_staged) == len(deleted_staged) == 0)
        changes_not_staged_absent = (len(untracked) == len(modified_unstaged) == len(deleted_unstaged) == 0)

        # Checking if there are any changes to be displayed
        if changes_to_be_committed_absent and changes_not_staged_absent:
            print(Fore.YELLOW + "nothing to commit, working tree clean\n")
            return

        # Changes to be committed
        if changes_to_be_committed_absent:
            print(Fore.YELLOW + "No changes added to commit")
        else:
            print(Fore.YELLOW + "Changes to be committed:")
            for file in new_staged:
                print(Fore.GREEN + "\t     new:\t" + file)
            for file in modified_staged:
                print(Fore.GREEN + "\tmodified:\t" + file)
            for file in deleted_staged:
                print(Fore.GREEN + "\t deleted:\t" + file)
        print()

        # Changes not staged for commit
        if changes_not_staged_absent:
            print(Fore.YELLOW + "All changes have been staged")
        else:
            print(Fore.YELLOW + "Changes not staged for commit:")
            for file in modified_unstaged:
                print(Fore.RED + "\tmodified:\t" + file)
            for file in deleted_unstaged:
                print(Fore.RED + "\t deleted:\t" + file)
        print()

        if len(untracked)!=0:
            print(Fore.YELLOW + "Untracked files:")
            for file in untracked:
                print(Fore.RED + '\t' + file)
        print()
        return

    # Function to display changes to be committed
    # Compares index with previous commit's main tree
    def get_staged(new_staged: list, modified_staged: list, deleted_staged: list, index_fname: list, index_fhash: list, prev_index_fname: list, prev_index_fhash: list):

        # Iterating through files in index_fname
        for i in range(len(index_fname)):
            fname = index_fname[i]
            fhash = index_fhash[i]

            if fname not in prev_index_fname:
                # File from index is not in prev_index
                new_staged.append(fname)
            elif prev_index_fhash[prev_index_fname.index(fname)]!=fhash:
                # File present in prev_index is different from one in index
                modified_staged.append(fname)
            else:
                # File is the same as one present in prev_index
                continue

        # Iterating through files in prev_index_fname
        for i in range(len(prev_index_fname)):
            fname = prev_index_fname[i]
            if fname not in index_fname:
                # File from prev_index is not in index
                deleted_staged.append(fname)
        return
    
    # Compares index with current working directory
    def get_untracked(untracked: str, index_fname: list, path: str, main_dir: str):
        # Here path is the path of the directory relative to main_dir
        # This recursive function is always in the main_dir
        # Iteratively scanning path directory
        for file in os.scandir(path):
            if os.path.isdir(file) and (file.name[0]=='.' or file.name[0]=='_'):
                # file is a hidden file or system file
                continue
            elif os.path.isdir(file):
                # file is a directory
                # Checking if there is any file staged from this directory
                # Since file.path starts with '.\', we compare from 3rd letter of the string
                prefix_len = len(file.path) - 2
                is_present = False
                for fname in index_fname:
                    if fname[:prefix_len]==file.path[2:]:
                        is_present = True
                        break
                if not is_present:
                    untracked.append(file.path[2:] + '\\')
                else:
                    Status.get_untracked(untracked, index_fname, file.path, main_dir)
            elif os.path.isfile(file):
                # Since file.path starts with '.\', we compare from 3rd letter of the string
                if file.path[2:] not in index_fname:
                    # File is not present in the index
                    untracked.append(file.path[2:])
        return
    
    # Compares index with current working directory
    # Function is called from the main working dir
    def get_modified_deleted_unstaged(modified_unstaged: list, deleted_unstaged: list, index_fname: list, index_fhash):
        # Iterating through files in index_fname
        for i in range(len(index_fname)):
            fname = index_fname[i]
            fhash = index_fhash[i]
            if not os.path.exists(fname):
                # File was deleted but present in the index
                deleted_unstaged.append(fname)
            elif Blob.get_hash(fname)!=fhash:
                # File present in index is different from one in working directory
                modified_unstaged.append(fname)
            else:
                # File is the same as one present in working directory
                continue
        return
# Class definition ends