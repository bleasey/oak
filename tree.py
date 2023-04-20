import os
import hashlib
from blob import Blob

# Class definition begins
class Tree(staticmethod):

    def create_tree(path: str, main_dir: str):
        '''
        Tree structure:
        Line1..........."tree"
        Line2 onwards...<object type>  <name>  <hash>....:(separated by tab)
        '''
        initial_dir = os.getcwd()
        os.chdir(main_dir)
        tree_content = "tree"

        # We add <object type>  <name>  <hash> for every blob/tree added
        for file in os.scandir(path):
            if os.path.isdir(file) and (file.name[0]=='.' or file.name[0]=='_'):
                # file is a hidden file or system file
                continue  
            elif os.path.isdir(file):
                fname = file.name
                fhash = Tree.create_tree(file.path, main_dir)
                tree_content += "\n" + "tree\t" + fname + "\t" + fhash
                continue
            elif os.path.isfile(file):
                fname = file.name
                fhash = Blob.create_blob(file.path, main_dir)
                tree_content += "\n" + "blob\t" + fname + "\t" + fhash

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