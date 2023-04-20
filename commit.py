import os
import hashlib
import datetime
from blob import Blob
from tree import Tree

# Class definition begins
class Commit(staticmethod):

    def create_commit(comment: str):
        '''
        Tree structure:
        Line1..........."commmit"
        Line2...........<hash of main dir tree>
        Line3...........<hash of parent commit>
        Line4...........<timestamp>
        Line5...........<comment>
        '''

        '''
        In this version of the system, there isn't any add
        implementation. Commit includes all non dir files
        present in the main directory in a commit.
        '''
        
        main_dir = os.getcwd()
        commit_content = "commit"

        # Adding hash of main dir tree
        tree_hash = Tree.create_tree(main_dir, main_dir)
        commit_content += "\n" + tree_hash

        # Adding hash of parent commit
        # Reading hash stored in .oak\head
        os.chdir(".oak")
        if not os.path.exists("HEAD"):
            # No previous HEAD exists
            commit_content += "\n" + "NULL"
        else:
            with open("HEAD", 'r') as file:
                head_hash = file.readline()
                assert len(head_hash)==40
                commit_content += "\n" + head_hash

        # Adding date and time info
        commit_content += "\n" + Commit.get_curr_timestamp()

        # Adding commit comment
        commit_content += "\n" + comment

        # Commit content completed

        # Hashing the binary encoded content
        hash_object = hashlib.sha1(commit_content.encode('utf-8'))
        hash_str = hash_object.hexdigest()
        hash_prefix = hash_str[:2]
        hash_suffix = hash_str[2:]

        # Creating commit object folder and file in .git/objects
        # We are currently in ".oak"
        os.chdir("objects")

        if not os.path.exists(hash_prefix):
            os.mkdir(hash_prefix)
        os.chdir(hash_prefix)

        if not os.path.exists(hash_suffix):
            with open(hash_suffix, 'w') as file:
                file.write(commit_content)

        # Updating 
        os.chdir(os.path.join(main_dir, ".oak"))
        with open("HEAD", 'w') as file:
            file.write(hash_str)

        os.chdir(main_dir)
        return hash_str


    def get_tree_hash(hash_str: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak", "objects", hash_str[:2]))
        with open(hash_str[2:], 'r') as file:
            # Read first line, NULL char at the end is excluded
            tree_hash = file.readlines()[1][:-1]
            assert len(tree_hash)==40
        os.chdir(initial_dir)
        return tree_hash


    def get_parent_hash(hash_str: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak", "objects", hash_str[:2]))
        with open(hash_str[2:], 'r') as file:
            # Read second line, NULL char at the end is excluded
            parent_hash = file.readlines()[2][:-1]
            #assert (len(parent_hash)==40 or parent_hash=="NULL")
        os.chdir(initial_dir)
        return parent_hash


    def get_date(hash_str: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak", "objects", hash_str[:2]))
        with open(hash_str[2:], 'r') as file:
            # Read third line, NULL char at the end is excluded
            date = file.readlines()[3][:-1]
        os.chdir(initial_dir)
        return date


    def get_comment(hash_str: str, main_dir: str):
        initial_dir = os.getcwd()
        os.chdir(os.path.join(main_dir, ".oak", "objects", hash_str[:2]))
        with open(hash_str[2:], 'r') as file:
            # Read fourth line fully
            comment = file.readlines()[4]
        os.chdir(initial_dir)
        return comment

    def get_curr_timestamp():
        now = datetime.datetime.now()
        day_of_week = now.strftime("%a")
        month_name = now.strftime("%b")
        date = now.strftime("%d")
        time = now.strftime("%H:%M:%S")
        year = now.strftime("%Y")
        timestamp = f"{day_of_week} {month_name} {date} {time} {year}"
        return timestamp

# Class definition ends