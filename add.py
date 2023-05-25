import os
import hashlib
from blob import Blob
from colorama import Fore, init

# Auto reset colour scheme
init(autoreset=True)

# Funtion definitions

'''
Index structure:
Line1 onwards...<relative file path>...tab...<hash>
'''

def add(input_str: str):
    # This function is always called from the main directory
    main_dir = os.getcwd()

    # Checks if index file exists
    if not os.path.exists(os.path.join(".oak", "index")):
        os.chdir(".oak")
        with open('index', 'w') as index:
            pass
    os.chdir(main_dir)

    # Splitting input_str to get the individual files to be added
    arr = input_str.split()

    # Getting content stored inside index
    os.chdir(".oak")
    with open('index', 'r') as index:
        index_content = index.readlines()
    os.chdir(main_dir)

    # Iterating through the files in arr
    for file in arr:
        if file == '.' or file == '*':
            # Adds all files in the main dir into the index
            # Passing the directory itself as the first parameter
            index_content = add_all(".", index_content, main_dir)
            # Overwriting
        elif os.path.isdir(file):
            # Adding all files in that directory
            index_content = add_all(file, index_content, main_dir)
        elif os.path.isfile(file):
            # Creating the file blob
            fhash = Blob.create_blob(file, main_dir)

            # Flag to determine if file exists in the index
            file_found = False

            for i in range(0, len(index_content)):
                line_content = index_content[i].split('\t')
                # First word contains relative path with filename
                if line_content[0] == file:
                    file_found = True
                    # Replacing hash with newer one
                    # Hash is the last 40 characters of a line
                    # -41 represent the hash and '\n'
                    index_content[i] = index_content[i][:-41] + fhash + '\n'
                    break
            
            if not file_found:
                # Adding the required string to index_content
                index_content.append(str(file + "\t" + fhash + '\n'))
        else:
            # Either file deletion should be staged or file does not exist
            is_present = False
            for i in range(0, len(index_content)):
                line_content = index_content[i].split('\t')
                # First word contains relative path with filename
                if line_content[0][:len(file)] == file:
                    # Removing the file i.e. staging the deletion
                    is_present = True
                    index_content.pop(i)
                    # We dont break here as we want to remove all subfiles recursively
            if not is_present:
                print(Fore.YELLOW + file + " -> No such file or directory exists")


    
    # Updating the content of index
    os.chdir(os.path.join(main_dir, '.oak'))
    with open('index', 'w') as index:
        new_content = ''
        for line in index_content:
            new_content += line
        # Writing new_content into index
        index.write(new_content)
    os.chdir(main_dir)
    return
    


def add_all(path: str, index_content: str, main_dir: str):
    # Here path is the absolute path of the directory
    initial_dir = os.getcwd()
    # We change to main_dir since the path given is relative to it
    os.chdir(main_dir)
    for file in os.scandir(path):
        if os.path.isdir(file) and (file.name[0]=='.' or file.name[0]=='_'):
            # file is a hidden file or system file
            continue  
        elif os.path.isdir(file):
            # file is a directory
            # file.path returns the 'path' passed into os.scandir() + file.name
            index_content = add_all(file.path, index_content, main_dir)
        elif os.path.isfile(file):
            # Creating the file blob
            fname = file.name
            fhash = Blob.create_blob(file.path, main_dir)

            # Flag to determine if file exists in the index
            file_found = False

            for i in range(0, len(index_content)):
                line_content = index_content[i].split('\t')
                # First word contains the file's relative path
                if line_content[0] == file.path:
                    file_found = True
                    # Replacing hash with newer one
                    # Hash is the last 40 characters of a line
                    # -41 represent the hash and '\n'
                    index_content[i] = index_content[i][:-41] + fhash + '\n'
                    break
            
            if not file_found:
                # Adding the required string to index_content
                index_content.append(file.path + "\t" + fhash + '\n')

    os.chdir(initial_dir)
    # Returning the content
    return index_content

