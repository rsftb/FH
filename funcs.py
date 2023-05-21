"""
Functions used by filehandler.py
"""

import shutil
import time
import os
import colorama as clr



def typing(sentence: str, slp: float, prtend='', newln=False):
    "Customizable typewriter effect for console printing"

    for letter in sentence:
        time.sleep(slp/2)
        print(letter, end=prtend, flush=True)
        time.sleep(slp/2)

    if newln:
        print()

    return ''


#? printing what color
def change_directory():
    """
    Opens the cdir interface.\n
    case insensitive
    """

    typing(clr.Fore.GREEN + " \\\\ Change directory to? (case insensitive) => " + os.getcwd() + clr.Style.RESET_ALL, 0.01, newln=True)

    to = input(typing(clr.Fore.GREEN + "  || " + clr.Style.RESET_ALL + "C:\\", 0.01))
    goto = f"c:\\{to}"

    try:
        os.chdir(goto)
        typing(clr.Fore.GREEN + f" // {os.getcwd()}" + clr.Style.RESET_ALL, 0.01, newln=True)
    except FileNotFoundError:
        print(f"{clr.Fore.GREEN} // Path not found. {clr.Style.RESET_ALL}")
        return False

    return True


def show_directory(case: int):
    "Displays directory content by filter, prepends folders with `>>`"

    print(clr.Fore.GREEN + os.getcwd() + clr.Style.RESET_ALL)

    if not os.listdir():
        print(clr.Fore.BLACK + " # EMPTY DIRECTORY" + clr.Style.RESET_ALL)

    else:
        try:

            if case == 0: #* SHOWING FILES AND DIRECTORIES
                for item in os.listdir():
                    if os.path.isdir(item):
                        print(clr.Fore.RED + ">>" + clr.Style.RESET_ALL + item)
                    else:
                        print(clr.Fore.LIGHTBLACK_EX + item + clr.Style.RESET_ALL)

            elif case == 1: #* SHOWING DIRECTORIES
                for item in os.listdir():
                    if os.path.isdir(item):
                        print(clr.Fore.RED + ">>" + clr.Fore.WHITE + item + clr.Style.RESET_ALL)

            elif case == 2: #* SHOWING FILES
                for item in os.listdir():
                    if os.path.isfile(item):
                        print(clr.Fore.LIGHTBLACK_EX + item + clr.Style.RESET_ALL)

        except PermissionError as err:
            print(f"PermissionError | Not Authorized \n{err}")

    return ''


def move_directory():
    "Execution opens an interface for moving through local files"

    typing(clr.Fore.LIGHTGREEN_EX + ":: :: :: ::" + clr.Style.RESET_ALL, 0.01, newln=True)
    display_valve = 0
    while True:

        show_directory(display_valve)
        select = input(typing(clr.Fore.LIGHTGREEN_EX + ":: " + clr.Style.RESET_ALL, 0.01)).lower()

        if not select:
            print()
            continue

        if select in ('exit', 'e'): #* Exit
            typing(clr.Fore.LIGHTGREEN_EX + "::", 0.01, newln=True)
            typing(":: :: :: " + os.getcwd() + clr.Style.RESET_ALL, 0.01, newln=True)
            return True

        print()

        if select in '-files': #* Swap content display filter
            if display_valve == 0:
                print(clr.Fore.GREEN + "SHOWING DIRECTORIES" + clr.Style.RESET_ALL)
            elif display_valve == 1:
                print(clr.Fore.GREEN + "SHOWING FILES" + clr.Style.RESET_ALL)
            elif display_valve == 2:
                print(clr.Fore.GREEN + "SHOWING FILES AND DIRECTORIES" + clr.Style.RESET_ALL)

            display_valve += 1
            display_valve = display_valve % 3


        elif select == '-up' or select == '-u': #* Move up a directory
            os.chdir('..')

        elif select == '-mkdir' or select == '-mk': #* Create a named folder
            print(clr.Fore.GREEN + "Name of folder?" + clr.Style.RESET_ALL)
            folder = input(typing(clr.Fore.LIGHTGREEN_EX + ":: " + clr.Style.RESET_ALL, 0.01)).lower()

            if not folder:
                print(f"{clr.Fore.RED}-- Warning: Empty string given{clr.Style.RESET_ALL}\n")
                continue

            try:
                os.mkdir(f'{os.getcwd()}/{folder}')
            except FileExistsError as err:
                print(f"FileExistsError | '{folder}' \n{err}")
            except OSError as err:
                print(f"OSError | Did the input contain special characters? \n{err}")

            print()


        elif select == '-remove' or select == '-r': #* Remove a named item in the current directory
            print(clr.Fore.GREEN + "Name of item to remove?" + clr.Style.RESET_ALL)
            folder = input(typing(clr.Fore.LIGHTGREEN_EX + ":: " + clr.Style.RESET_ALL, 0.01)).lower()

            if not folder:
                print(f"{clr.Fore.RED}-- Warning: Empty string given{clr.Style.RESET_ALL}\n")
                continue

            print(f"{clr.Fore.RED}\nAre you sure you want to remove `{folder}`?{clr.Style.RESET_ALL}")
            answer = input(typing(clr.Fore.RED + ":: " + clr.Style.RESET_ALL, 0.07)).lower()

            if answer == "no" or answer in "no" or answer != "yes" or answer not in "yes":
                print()
                continue

            try:
                shutil.rmtree(f'{os.getcwd()}/{folder}')
            except FileNotFoundError as err:
                print(f"FileNotFoundError \n{err}")
            except OSError as err:
                print(f"OSError \n{err}")

            print()


        else: #* If input isn't command, try to enter a directory
            goto = f"\\{select}"
            try:
                os.chdir(f"{os.getcwd()}{goto}")
            except FileNotFoundError as err:
                print(f"FileNotFoundError \n{err}\n")
            except OSError as err:
                print(f"OSError | Bad input \n{err}\n")


        continue


def jump_directory():
    """
    Jumps back to a select /directory/ in the tree by typing the name.\n
    Case Sensitive.
    """

    typing(clr.Fore.CYAN + " \\\\ Jump to? (Case Sensitive) => " + os.getcwd() + clr.Style.RESET_ALL, 0.01, newln=True)
    parent = input(typing(clr.Fore.CYAN + "  || " + clr.Style.RESET_ALL + "\\", 0.01))
    cwd_split = os.getcwd().split("\\")

    if not parent or all(letter == ' ' for letter in parent):
        typing(clr.Fore.CYAN + " // Jump failed, input is empty" + clr.Style.RESET_ALL, 0.005, newln=True)
        return None

    if parent not in cwd_split:
        typing(clr.Fore.CYAN + f" // Jump failed, couldn't find directory '{parent}' in parent directories" + clr.Style.RESET_ALL, 0.005, newln=True)
        return False

    new_path = []
    new_dir_idx = cwd_split.index(parent)

    for idx, dir_name in enumerate(cwd_split):
        if idx <= new_dir_idx:
            new_path.append(dir_name)
        else:
            break

    new_path = "\\".join(new_path)
    os.chdir(new_path)
    typing(clr.Fore.CYAN + f" // {os.getcwd()}" + clr.Style.RESET_ALL, 0.005, newln=True)

    return True


def exec_code():
    """Allows you to execute raw Python code using `exec()`"""

    typing(clr.Fore.RED + "########" + clr.Style.RESET_ALL, 0.01, newln=True)

    while True: #* Single line mode
        line = input(typing(clr.Fore.RED + "#  >> " + clr.Style.RESET_ALL, 0.01))

        if line != "-block" and line != "exit": #* If not a command, run as a single line of code
            script = line

        elif line == "exit":
            typing(clr.Fore.RED + "########" + clr.Style.RESET_ALL, 0.01, newln=True)
            return True

        elif line == "-block":
            script = ''''''

            while True: #* Block code mode
                line = input(typing(clr.Fore.RED + "# >>> " + clr.Style.RESET_ALL, 0.01))
                if line == "-block":
                    break
                script += line
                script += "\n"

        else: #* Not a recognized input, so ignore
            continue

        try: #* Execution of written code
            typing(clr.Fore.LIGHTRED_EX + "''''''''" + clr.Style.RESET_ALL, 0.01, newln=True)
            exec(script)
        except Exception as warning:
            typing(clr.Fore.LIGHTWHITE_EX + f":: {warning}" + clr.Style.RESET_ALL, 0.01, newln=True)
        finally:
            typing(clr.Fore.LIGHTRED_EX + "........" + clr.Style.RESET_ALL, 0.01, newln=True)


#typing("Mary had a little lamb", 0.09)
