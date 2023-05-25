import os
import hashlib
from blob import Blob

# Class definition begins
class Tree(staticmethod):
    '''
    Tree structure:
    Line1..........."tree"
    Line2 onwards...<object type>  <name>  <hash>....:(separated by tab)
    '''
    
    def create_index_tree(main_dir: str):
        '''
        Function to create a tree out of contents in the index
        We pass the index contents to create_tree in a sorted manner
        '''
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak"))
        with open('index', 'r') as index:
            index_content = index.readlines()
        
        # Splitting the text for each string in index_content to get name and hash
        # Removing the final character '\n' from 2nd word for elements in index_content
        for i in range(len(index_content)):
            index_content[i] = index_content[i].split('\t')
            index_content[i][1] = index_content[i][1][:-1]

        # Sorting elements from index_content according to the first word i.e file name
        index_content.sort()
        os.chdir(initial_dir)
        return Tree.create_tree(index_content, main_dir)

    def create_tree(arr: list, main_dir: str):
        '''
        Function to create a tree object out of 'arr': a list having
        a subset of lines from the index that belong to the same folder.
        Line format: <relative file path>...tab...<hash>
        We assume that arr is sorted according to the relative file paths.
        '''
        initial_dir = os.getcwd()
        os.chdir(main_dir)
        tree_content = "tree"

        # We add <object type>  <name>  <hash> for every blob/tree added
        # Iterating along arr by i
        i=0
        while(i<len(arr)):
            # fname contains the relative path inside the folder
            fname = arr[i][0]
            fhash = arr[i][1]

            # If fname contains '/' or '\' it refers to a file inside another subdirectory
            # Else it is added as a blob to tree_content
            if fname.__contains__('\\') or fname.__contains__('/'):
                # Position of '\' or '/'
                idx = fname.find('\\')
                # If idx is -1, fname does not contain '\'
                if idx==-1:
                    idx = fname.find('/')

                dir_name = fname[:idx]

                # Recursively creating a tree out of dir_name
                new_arr = []

                # Continuing along arr to find all files contained by dir_name
                while i<len(arr) and arr[i][0][:idx]==dir_name:
                    fname = arr[i][0]
                    fhash = arr[i][1]
                    remaining_path = fname[idx+1:]
                    new_arr.append([remaining_path, fhash])
                    i+=1

                tree_hash = Tree.create_tree(new_arr, main_dir)
                tree_content += "\n" + "tree\t" + dir_name + "\t" + tree_hash
                continue
            else:
                # File exists in the current directory
                tree_content += "\n" + "blob\t" + fname + "\t" + fhash
                i+=1

        # Hashing the binary encoded content
        hash_object = hashlib.sha1(tree_content.encode('utf-8'))
        hash_str = hash_object.hexdigest()
        hash_prefix = hash_str[:2]
        hash_suffix = hash_str[2:]

        # Creating commit tree folder and file in .git/objects
        os.chdir(os.path.join(".oak", "objects"))

        if not os.path.exists(hash_prefix):
            os.mkdir(hash_prefix)
        os.chdir(hash_prefix)

        if not os.path.exists(hash_suffix):
            with open(hash_suffix, 'w') as file:
                file.write(tree_content)

        os.chdir(initial_dir)
        return hash_str
# Class definition ends