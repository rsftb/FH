"""
The main script.
Executions runs the program.
"""

import os
import sys
import colorama as clr
from funcs import typing, change_directory, show_directory, move_directory, jump_directory, exec_code

clr.init()



# :: help -> Pages displayed by the `help` command
#   Format is one string per command
help_pages = {
    1: {
        "help": "Displays this menu",
        "move": "Move through directories",
        "jump": "Jump to a higher directory",
        "cdir": "Change the current directory",
        "sdir": "Print all files in the current directory",
    },

    2: {
        "cls": "Clears the screen",
        "pdir": "Prints the current working directory",
        "exec": "Execute Python code"
    }
}

# :: help (cmd) -> One line description of the command
#   Format is one string per command
help_header = {
    "help": "Opens the help menu",
    "move": "Opens the move interface to navigate folders",
    "jump": "Jump to a higher directory in your path by typing the name of the folder",
    "cdir": "Write the full path you want to enter",
    "sdir": "Prints all items in the current directory",
    "cls": "(cls) clears the screen",
    "pdir": "Print the current directory",
    "exec": "Opens the exec interface to execute Python code"
}

# :: help (cmd) -> Extra information if needed
#   Format is one list index per string printed
help_subheader = {
    "help": None,
    "move": None,
    "jump": ["(e.g. c:\\Users\\myself\\Documents >> \\myself >> c:\\Users\\myself)"],
    "cdir": ["(e.g. Users\\myself\\Workspace\\Python)"],
    "sdir": None,
    "cls": None,
    "pdir": None,
    "exec": None,
}

# :: help (cmd) -> Displays subcommands if present
#   Tree format -> ["(sub_cmd)", "(description)", "(sub_cmd)", "(description)"]
help_subcom = {
    "help": None,
    "move": ["-up", "Move up one directory", "-files", "Toggles item display mode", "-mkdir", "Creates a folder in the current directory", "-remove", "Lets you remove a file", "exit", "Exit"],
    "jump": None,
    "cdir": None,
    "sdir": None,
    "cls": None,
    "pdir": None,
    "exec": ["-block", "Allows you to write multi-line code. Use -del to delete the block of code. Remember to indent!"],
}


def print_help(title):
    """Executes on any help command"""

    #* HEADER // Always prints
    typing(clr.Fore.YELLOW + f":: {title} - {help_header[title]}" + clr.Style.RESET_ALL, 0.01, newln=True)

    #* SUB HEADER // Could print
    if help_subheader[title] is not None:
        for subheader in range(0, len(help_subheader[title])):
            typing(clr.Fore.YELLOW + f":: {help_subheader[title][subheader]}" + clr.Style.RESET_ALL, 0.01, newln=True)

    #* SUB COMMANDS // Could print
    if help_subcom[title] is not None:
        for i in range(0, len(help_subcom[title])-1, 2):
            typing(clr.Fore.YELLOW + ":: " + clr.Style.RESET_ALL + help_subcom[title][i] + clr.Fore.RED + " >> " + clr.Style.RESET_ALL + help_subcom[title][i+1], 0.01, newln=True)



class FileHandler():
    """
    Main class (singleton)
    This is the skeleton of the program
    Main functions are called or present inside this class
    Initializes at class instantiation
    """

    __instance = None

    @staticmethod
    def getInstance():
        """Static Access Method"""
        if FileHandler.__instance is None:
            FileHandler()

        return FileHandler.__instance

    def __init__(self, debug_no_play=False):
        self.initializing = True


        if FileHandler.__instance is not None:
            raise UserWarning("Only one instance of FileHandler allowed")

        FileHandler.__instance = self

        self.initializing = False

        if not debug_no_play:
            self.window_new(1)
        else:
            return

    def window_new(self, mode):
        """Start-up program"""
        os.system("cls||clear")

        try:
            os.chdir(sys.path[0])
        except Exception as exc: #!
            raise UserWarning("Could not initialize current directory in new_open()") from exc

        if mode == 0:
            color_1 = clr.Fore.LIGHTWHITE_EX
            color_2 = clr.Fore.BLACK
        else:
            color_1 = clr.Fore.BLACK
            color_2 = clr.Fore.LIGHTWHITE_EX

        typing(color_1 + "FH - 2023\n" + clr.Style.RESET_ALL, 0.1, newln=True)
        typing(color_2 + os.getcwd() + clr.Style.RESET_ALL, 0.01, newln=True)

        print()

        self.main()


    def main(self):
        """Input element for request handler"""
        
        while True:
            select = input(typing(clr.Fore.BLUE + ":: " + clr.Style.RESET_ALL, 0.01)).lower()
            if not select:
                continue

            self.request(select)


    def request(self, req):
        """Pre-processes and/or handles requests"""
        request = req.split(" ")
        run_args = False
        argument = None

        if len(request) > 1:
            run_args = True
            argument = request[1]

        #* HELP
        if request[0] in "help" or request[0] in "cmd":
            if not run_args:
                self.display_help(1)
            else:
                try:
                    argument = int(argument)
                    self.display_help(argument)
                except ValueError:
                    try:
                        print_help(argument)
                    except KeyError:
                        typing(clr.Fore.YELLOW + f"-- help ({argument}) not found" + clr.Style.RESET_ALL, 0.01, newln=True)
                        return False
                except TypeError:
                    typing(clr.Fore.YELLOW + "-- Type Error" + clr.Style.RESET_ALL, 0.01, newln=True)
                    return 0

        #* HELLO WORLD
        elif request[0] in "hello world":
            print(" # hi! " )

        #* MOVE
        elif request[0] == "move":
            move_directory()

        #* JUMP
        elif request[0] == "jump":
            jump_directory()

        #* CDIR
        elif request[0] in "cdir" or request[0] in "changedir":
            change_directory()

        #* SDIR
        elif request[0] in "sdir" or request[0] == "showdir":
            if not run_args:
                show_directory(0)

            elif argument == 'd' or argument in "directory":
                show_directory(1)

            elif argument == 'f' or argument in "files":
                show_directory(2)

            elif argument == 'a' or argument in "all":
                show_directory(0)

            else:
                print(clr.Fore.GREEN + "-- Unknown argument for sdir" + clr.Style.RESET_ALL)
                return False


        #* PRINT DIRECTORY NAME
        elif request[0] in "pdir" or request[0] == "printdir":
            print(" # " + clr.Fore.GREEN + os.getcwd() + clr.Style.RESET_ALL)

        #* CLEAR
        elif request[0] in "cls" or request[0] == "clear":
            os.system("cls||clear")

        #* PRINT
        elif request[0] == "prt" or request[0] == "print":
            if not request[1]:
                return False
            print(" # " + " ".join(request[1:]), end="\n")

        #* EXEC
        elif request[0] == "exec":
            exec_code()

        #* EXIT
        elif request[0] in "exit":
            self.window_end()

        else:
            return False

        return True


    def display_help(self, page=1):
        """Prints a page of the help menu >> `:: help 2`\n
        Prints a description of a command >> `:: help cdir`"""
        if page > 2:
            typing(clr.Fore.YELLOW + f"-- help {page}/2 doesn't exist" + clr.Style.RESET_ALL, 0.007, newln=True)
            return 0

        typing(clr.Fore.YELLOW + f":: :: :: HELP {page}/2" + clr.Style.RESET_ALL, 0.007, newln=True)

        for cmd, desc in help_pages[page].items():
            typing(clr.Fore.YELLOW + ":: " + clr.Style.RESET_ALL + cmd + clr.Fore.RED + " >> " + clr.Style.RESET_ALL + desc, 0.007, newln=True)

        typing(clr.Fore.YELLOW + ":: " + clr.Style.RESET_ALL + "use help (...) for help on specific commands", 0.007, newln=True)
        typing(clr.Fore.YELLOW + ":: ::" + clr.Style.RESET_ALL, 0.01, newln=True)

        return True

    def window_end(self):
        """Quits the program"""
        typing(clr.Fore.LIGHTRED_EX + "::::::::" + clr.Style.RESET_ALL, 0.015, newln=True)
        quit()



if __name__ == "__main__":
    FH = FileHandler(debug_no_play=False)

    print("\n EXIT")
