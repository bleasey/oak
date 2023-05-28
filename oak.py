import sys
import os
from init import init
import add
from commit import Commit
from log import Log
from status import Status
from restore import Restore

initial_dir = os.getcwd()

def main():
    command = sys.argv[1]

    if not (command =='init' or command =='help') and not os.path.exists(os.path.join(os.getcwd(), '.oak')):
        print("Error: No repository found")
    elif command == 'init':
        init()
    elif command == 'add' and len(sys.argv) >= 3:
        args = ' '.join(sys.argv[2:])
        add.add(args)
    elif command == 'commit' and len(sys.argv) >= 3:
        args = ' '.join(sys.argv[2:])
        Commit.create_commit(args)
    elif command == 'status' and len(sys.argv) == 2:
        Status.get_status()
    elif command == 'log' and len(sys.argv) == 2:
        Log.log(os.getcwd())
    elif command == 'log' and len(sys.argv) == 3 and sys.argv[2] == 'oneline':
        Log.short_log(os.getcwd())
    elif command == 'restore' and len(sys.argv) == 4:
        arg1 = sys.argv[2]
        arg2 = sys.argv[3]
        Restore.restore(arg1, arg2, os.getcwd())
    elif command == 'help':
        print("--> oak init\nInitialises an empty repository\n")
        print("--> oak add arg1 arg2 arg3......\nAdds files or/and subdirectories into the staging area. The arguments after add can represent either a file or a directory\n")
        print("--> oak commit arg1 arg2.....\nMakes a commit from the files in the staging area. The arguments after commit can represent the commit message\n")
        print("--> oak log\nDisplays commit history and their details\n")
        print("--> oak log oneline\nSimilar to oak log but displays commit info concisely\n")
        print("--> oak restore arg1 arg2\nCompletely restores a file or directory to how it was in a previous commit. arg1 is the file/directory path, arg2 is the required commit hash\n")
    else:
        print("Error: Invalid command")
        print("Try: oak help")
    os.chdir(initial_dir)

if __name__ == '__main__':
    main()