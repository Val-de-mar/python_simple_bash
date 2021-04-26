import os
from os import path
import re
import subprocess
import sys


class NonDirName(Exception):
    """
    path is not path to directory
    """


class InvalidSyntax(Exception):
    """
    Not correct syntax
    """


class InvalidArgument(Exception):
    """
    Not correct argument
    """


class NonFileName(Exception):
    """
    path is not path to file
    """


class InvalidDir(Exception):
    """
    Not correct directory
    """


class CurrentDirDeleting(Exception):
    """
    Deleting of working directory
    """


class Executer:
    def __init__(self):
        pass

    def chdir(self, subcommand):
        """
        changes directory
        """
        if isinstance(self, int):
            raise SyntaxError

        place = path.expanduser(subcommand[0])
        if os.path.isdir(place):
            os.chdir(place)
        else:
            raise NonDirName

    def listdir(self, aim_path: str, flags: str = ""):
        """
        list directory content
        """
        if isinstance(self, int):
            raise SyntaxError
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
        result += "\n\033[37m"
        return result

    def copy(self, input_file: str, output: str):
        """
        copies file
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isdir(path.dirname(output)):
            if path.dirname(output) != "":
                raise NonDirName
        if not path.isfile(input_file):
            raise InvalidSyntax
        if path.isdir(output):
            output += "/"
            output += path.basename(input_file)
        os.system("cp " + input_file + " " + output)

    def move(self, input_file: str, output: str):
        """
        moves file
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isdir(path.dirname(output)):
            if path.dirname(output) != "":
                raise NonDirName
        if not path.isfile(input_file):
            raise InvalidSyntax
        if path.isdir(output):
            output += "/"
            output += path.basename(input_file)
        os.system("mv " + input_file + ' ' + output)

    def remove_file(self, filename: str):
        """
        removes file
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isfile(filename):
            raise NonFileName
        os.remove(filename)

    def remove_directory(self, directory_name: str):
        """
        removes empty directory
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isdir(directory_name):
            raise NonDirName
        if os.listdir(directory_name) != []:
            raise InvalidArgument
        os.removedirs(directory_name)

    def make_directory(self, dirname):
        """
        creates directory
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isdir(path.dirname(dirname)):
            raise NonDirName

        os.makedirs(dirname)

    def cat(self, filename):
        """
        prints file content
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isfile(filename):
            raise NonFileName
        file = open(filename, 'r')
        ans = file.read()
        file.close()
        return ans

    def touch(self, filename):
        """
        creates empty file
        """
        if isinstance(self, int):
            raise SyntaxError
        if not path.isdir(path.dirname(filename)):
            raise NonDirName
        if path.exists(filename):
            raise InvalidArgument
        file = open(filename, 'w')
        file.close()

    def subprocess(self, directory: str, subcommand: list,
                   stdin, stdout, stderr):
        """
        runs subprocess
        """
        if isinstance(self, int):
            raise SyntaxError
        os.chdir(directory)
        subprocess.run(subcommand, stdin=sys.stdin,
                       stdout=sys.stdout, stderr=sys.stderr)
