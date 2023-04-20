import os
import hashlib

# Class definition begins
class Blob(staticmethod):

    def create_blob(path: str, main_dir: str):
        '''
        Blob structure:
        Line1..........."blob"
        Line2 onwards...content
        '''
        initial_dir = os.getcwd()
        os.chdir(main_dir)

        name = os.path.basename(path)
        with open(path, 'r') as file:
            content = file.read()

        # Hashing the binary encoded content
        hash_object = hashlib.sha1(content.encode('utf-8'))
        hash_str = hash_object.hexdigest()
        hash_prefix = hash_str[:2]
        hash_suffix = hash_str[2:]

        # Creating commit blob folder and file in .git/objects
        os.chdir(os.path.join(".oak", "objects"))

        if not os.path.exists(hash_prefix):
            os.mkdir(hash_prefix)
        os.chdir(hash_prefix)

        if not os.path.exists(hash_suffix):
            with open(hash_suffix, 'w') as file:
                file.write("blob\n")
                file.write(content)

        os.chdir(initial_dir)
        return hash_str


    def get_content(hash_str: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(main_dir)

        # Asserting that hash is a 40 char shah1 hash
        assert len(hash_str)==40

        os.chdir(os.path.join(".oak", "objects", hash_str[:2]))
        with open(hash_str[2:], 'r') as file:
            assert file.read()[:4] == "blob"
            # Removing the 1st line: "blob\n" from file.read() i.e. first 5 characters
            content = file.read()[5:]

        os.chdir(initial_dir)
        return content
    
# Class definition ends