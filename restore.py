import os
import shutil
import hashlib
from blob import Blob
from commit import Commit
from colorama import Fore, init

# Auto reset colour scheme
init(autoreset=True)

# Class definition begins
class Restore(staticmethod):

    # Given hash of a commit, restore the file/folder to the file from that commit
    def restore(path: str, commit_hash: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(main_dir)

        assert len(commit_hash)==40

        if path == '.' or path == '*':
            # Replace everything
            for file in os.scandir(main_dir):
                # Getting object info
                object_list = Restore.get_object_list(path, commit_hash, main_dir)
                if object_list[0] == 'NULL':
                    continue

                # Proceeding if commit contains the file
                if file.name[0] == '.' or file.name[0] == '_':
                    pass
                elif os.path.isdir(file.path):
                    fpath = file.path
                    shutil.rmtree(fpath)
                    Restore.restore_object(object_list[0], fpath, object_list[2][:40], main_dir)
                elif os.path.isfile(file.path):
                    fpath = file.path
                    os.remove(fpath)
                    Restore.restore_object(object_list[0], fpath, object_list[2][:40], main_dir)
        else:
            # Getting object info
            object_list = Restore.get_object_list(path, commit_hash, main_dir)
            if object_list[0] == 'NULL':
                pass
            else:
                Restore.restore_object(object_list[0], path, object_list[2][:40], main_dir)
        os.chdir(initial_dir)
        return


    # Given object_hash and path, gets object content and creates it
    # Can be a file or a tree
    def restore_object(object_type: str, path: str, object_hash: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(main_dir)

        assert len(object_hash)==40

        if object_type == 'blob':
            # Case1: path represents a file
            # Reading content from referenced commit blob
            blob_content = Blob.get_content(object_hash, main_dir)
            # Writing content into given path file
            with open(path, 'w') as file:
                file.write(blob_content)

        elif object_type == 'tree':
            # Case2: path represents a directory
            # Getting tree contents
            with open(os.path.join('.oak', 'objects', object_hash[:2], object_hash[2:]), 'r') as file:
                # Removing the 1st line: "blob\n" from file.readlines()
                tree_content = file.readlines()[1:]

            # Deleting old directory, creating a new one with files present in the referenced commit
            if os.path.isdir(path):
                shutil.rmtree(path)
            os.mkdir(path)
            
            # Iterating through the commit files in the directory
            for line in tree_content:
                line_list = line.split('\t')
                if line_list[0] == 'tree':
                    # Creating the directory
                    os.mkdir(os.path.join(path, line_list[1]))
                    Restore.restore_object('tree', os.path.join(path, line_list[1]), line_list[2][:40], main_dir)
                elif line_list[0] == 'blob':
                    # Creating the file
                    with open(os.path.join(path, line_list[1]), 'w') as file:
                        pass
                    Restore.restore_object('blob', os.path.join(path, line_list[1]), line_list[2][:40], main_dir)

        else:
            print(Fore.YELLOW + path + " -> No such file or directory exists")

        os.chdir(initial_dir)


    '''
    Given a file/folder, function returns the hash of the tree containing it
    If file/folder is absent, returns 'NULL'
    Return format (one of the three):
    ['blob', path, hash]
    ['tree', path, hash]
    ['NULL']
    '''
    def get_object_list(path: str, commit_hash: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(main_dir)

        # Checking if commit ID exists
        if not os.path.exists(os.path.join('.oak', 'objects', commit_hash[:2], commit_hash[2:])):
            print(Fore.YELLOW + "Commit with given ID does not exist")
            return_list = ['NULL']
            os.chdir(initial_dir)
            return return_list
        # Getting content from the given commit
        tree_hash = Commit.get_tree_hash(commit_hash, main_dir)
        # Finding the corresponding blob
        fpath = path
        next_tree_hash = tree_hash
        while(True):
            # Getting the immediate file/folder name
            immediate_name = ""
            if '\\' in fpath:
                idx = fpath.index('\\')
                immediate_name = fpath[:idx]
            elif '/' in fpath:
                idx = fpath.index('/')
                immediate_name = fpath[:idx]
            # Getting tree contents
            with open(os.path.join('.oak', 'objects', next_tree_hash[:2], next_tree_hash[2:]), 'r') as file:
                # Removing the 1st line: "tree" from file.readlines()
                tree_content = file.readlines()
                assert tree_content[0] == "tree\n"
                tree_content = tree_content[1:]

            is_present = False
            for line in tree_content:
                line_list = line.split('\t')
                if line_list[1]==immediate_name:
                    is_present = True
                    # Corresponds to a tree
                    assert line_list[0]=='tree'
                    # Changing variables for next iteration
                    fpath = fpath[idx+1:]
                    next_tree_hash = line_list[2]
                    break
                elif line_list[1]==fpath:
                    is_present = True
                    # Changing directory before returning
                    os.chdir(initial_dir)
                    if line_list[0]=='blob':
                        return line_list # blob, name, hash    
                    elif line_list[0]=='tree':
                        return line_list # tree, name, hash
                    
            if not is_present:
                print(Fore.YELLOW + path + " -> No such file or directory exists in the given commit")
                print(commit_hash)
                return_list = ['NULL']
                os.chdir(initial_dir)
                return return_list
                
# Class definition ends