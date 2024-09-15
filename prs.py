#!/usr/bin/python3
import sys
#><
#create custom errors type
class LotArgumentsNumber(Exception):
    def __str__(self):
        return "Crashed: a lot of args"

class MissingArguments(Exception):
     def __str__(self):
         return "Crashed: missing args"

#parse command line arguments
def parse():
    args = [0,0] #this list is used to hold arguments
    if len(sys.argv) > 5:
        raise LotArgumentsNumber
    elif len(sys.argv) < 5:
        raise MissingArguments
    for arg in sys.argv:
        if arg == "-o":
            args[0] = sys.argv[sys.argv.index(arg) + 1]
        elif arg == "-f":
            args[1] = sys.argv[sys.argv.index(arg) + 1]
    return args

#Entry Point
if __name__ == "__main__":
    parse()
