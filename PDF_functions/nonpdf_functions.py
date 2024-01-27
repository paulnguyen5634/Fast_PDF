import os
import shutil
import sys
import json
from datetime import datetime
import re

def ToDoFolder():
    '''
    Looks into the ToDo folder
    '''

    # Goes into the directory of current python file
    cwd = os.getcwd()
    if os.path.isdir(cwd):
        ToDO_path = os.path.join(cwd, 'ToDo')

    folder = os.listdir(ToDO_path)

    # returns exception when folder is empty
    if len(folder) == 0:
        raise Exception('There are no files in the ToDo directory')

    folder_dict = {}
    for i in range(0, len(folder)):
        if folder[i][-4:] == '.txt':
            continue
        folder_dict[i] = folder[i]

    # prints the dictionary in a visually appealing manner
    print(json.dumps(folder_dict, indent=4, sort_keys=True))

    # Different error handling responses for incorrect user inputs
    while True:
        try:
            user_input = int(input('Please enter number corresponding to desired folder: '))
            filename = folder_dict[user_input]
            folder_path = os.path.join(ToDO_path, filename)
            print(folder_path)
            break

        # user inputs number not on list
        except KeyError:
            print('\n')
            print('Input value is not on list, please enter valid number printed on list')
            print('\n')
            print(json.dumps(folder_dict, indent=4, sort_keys=True))
            pass

        # user inputs string
        except ValueError:
            print('\n')
            print('Input value is a string, please pass in what is on printed list!')
            print('\n')
            print(json.dumps(folder_dict, indent=4, sort_keys=True))
            pass

        except KeyboardInterrupt:
            print('Stopping Program')
            sys.exit(0)
            break

    return folder_path

def tryint(s):
    """
    Return an int if possible, or `s` unchanged.
    """
    try:
        return int(s)
    except ValueError:
        return s

def alphanum_key(s):
    """
    Turn a string into a list of string and number chunks.

    alphanum_key("z23a")
    ["z", 23, "a"]

    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]

def human_sort(l):
    """
    Sort a list in the way that humans expect.
    """
    l.sort(key=alphanum_key)