import os
from os import path
import re

class NonDirName(Exception):
    pass


class InvalidSyntax(Exception):
    pass


class InvalidArgument(Exception):
    pass


class NonFileName(Exception):
    pass

class InvalidDir(Exception):
    pass

class CurrentDirDeleting(Exception):
    pass


class Executer:
    def __init__(self):
        pass

    def chdir(self, subcommand):

        place = path.expanduser(subcommand[0])
        if os.path.isdir(place):
            os.chdir(place)
        else:
            raise NonDirName

    def listdir(self, aim_path: str, flags: str = ""):
        if not path.isdir(aim_path):
            raise NonDirName
        aim_path += '/'
        list_dir = os.listdir(aim_path)
        if not re.match(r'a', flags):
            for name in enumerate(list_dir):
                if name[1][0] == ".":
                    list_dir.pop(name[0])
        ans = []
        for element in list_dir:
            if path.isdir(aim_path + element):
                preans = "\033[34m"
            elif os.access(aim_path + element, os.X_OK):
                preans = "\033[32m"
            else:
                preans = "\033[37m"
            ans += [preans + element]

        result = "\n".join(ans)
        result += "\033[37m"
        return result

    def copy(self, input: str, output: str):
        if not path.isdir(path.dirname(output)):
            if path.dirname(output) != "":
                raise NonDirName
        if not path.isfile(input):
            raise InvalidSyntax
        if path.isdir(output):
            output += "/"
            output += path.basename(input)
        os.system("cp " + input + " " + output)

    def move(self, input: str, output: str):
        if not path.isdir(path.dirname(output)):
            if path.dirname(output) != "":
                raise NonDirName
        if not path.isfile(input):
            raise InvalidSyntax
        if path.isdir(output):
            output += "/"
            output += path.basename(input)
        os.system("mv " + input + ' ' + output)

    def remove_file(self, filename: str):
        if not path.isfile(filename):
            raise NonFileName
        os.remove(filename)

    def remove_directory(self, directory_name: str):
        if not path.isdir(directory_name):
            raise NonDirName
        if os.listdir(directory_name) != []:
            raise InvalidArgument
        os.removedirs(directory_name)

    def make_directory(self, dirname):
        if not path.isdir(path.dirname(dirname)):
            raise NonDirName

        os.makedirs(dirname)

    def cat(self, filename):
        if not path.isfile(filename):
            raise NonFileName
        file = open(filename, 'r')
        ans = file.read()
        file.close()
        return ans

    def touch(self, filename):
        if not path.isdir(path.dirname(filename)):
            raise NonDirName
        if path.exists(filename):
            raise InvalidArgument
        file = open(filename, 'w')
        file.close()
