import os
import sys
from time import sleep
import re
from os import path


class NonDirName(Exception):
    pass


class InvalidSyntax(Exception):
    pass


class InvalidArgument(Exception):
    pass


class NonFileName(Exception):
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

    def listdir(self, aim_path: str):
        if not path.isdir(aim_path):
            raise NonDirName
        aim_path += '/'
        list_dir = os.listdir(aim_path)
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

    def make_directory(self, filename):
        if not path.isdir(path.dirname(filename)):
            if path.dirname(filename) != "":
                raise NonDirName

        os.makedirs(filename)


class FictiveStream:
    def __init__(self):
        self.list_str = []

    def write(self, *args):
        self.list_str += [' '.join(args)]

    def clear(self):
        self.list_str = []

    def toString(self, joint="\n"):
        return joint.join(self.list_str)


demiurge = Executer()


class Terminal:
    def __init__(self, out_stream=sys.stdout, err_stream=sys.stderr):
        self.home_dir = path.expanduser("~")
        self.last_dir = os.getcwd()
        self.cur_dir_name = os.getcwd()
        self.out_stream = out_stream
        self.err_stream = err_stream

    def deprivat(self, priv_path: str):
        if priv_path[0] == "~":
            place = path.expanduser(priv_path)
        elif priv_path[0] == "/":
            place = priv_path
        elif priv_path == "-":
            place = self.last_dir
        else:
            place = self.cur_dir_name + "/" + priv_path
        return path.realpath(place)

    def chdir(self, subcommand):
        if len(subcommand) != 1 or type(subcommand[0]) is not str:
            self.err_stream.write("too few arguments")
            return
        if len(subcommand) != 1 or type(subcommand[0]) is not str:
            self.err_stream.write("invalid syntax")
            return

        place = os.path.realpath(self.deprivat(subcommand[0]))
        if os.path.isdir(place):
            self.last_dir = self.cur_dir_name
            self.cur_dir_name = place
        else:
            self.err_stream.write("this dir doesn't exist")

    def cur_dir_name_short(self):
        ans = self.cur_dir_name
        if ans[0:len(self.home_dir)] == self.home_dir:
            ans = '~' + ans[len(self.home_dir):]
        return ans

    def listdir(self, subcommand: list):
        if not subcommand:
            subcommand.append(self.cur_dir_name)
        elif len(subcommand) != 1 or type(subcommand[0]) is not str:
            self.err_stream.write("too few arguments")
            return

        place = self.deprivat(subcommand[0])
        try:
            self.out_stream.write(demiurge.listdir(place))
        except NonDirName:
            self.err_stream.write("not directory name")

    def copy(self, subcommand):
        if not subcommand:
            subcommand[0] = self.cur_dir_name
        elif len(subcommand) != 2:
            self.err_stream.write("too few arguments")
            return

        input = self.deprivat(subcommand[0])
        output = self.deprivat(subcommand[1])
        try:
            demiurge.copy(input, output)
        except NonDirName:
            self.err_stream.write("incorrect input or output path")
        except InvalidSyntax:
            self.err_stream.write("incorrect syntax")

    def move(self, subcommand):
        if not subcommand:
            subcommand[0] = self.cur_dir_name
        elif len(subcommand) != 2:
            self.err_stream.write("too few arguments")
            return

        input = self.deprivat(subcommand[0])
        output = self.deprivat(subcommand[1])
        try:
            demiurge.move(input, output)
        except NonDirName:
            self.err_stream.write("incorrect input or output path")
        except InvalidSyntax:
            self.err_stream.write("incorrect syntax")

    def remove_file(self, subcommand):
        if len(subcommand) != 1:
            self.err_stream.write("invalid num of arguments")
            return
        elif not subcommand:
            subcommand[0] = self.cur_dir_name

        filename = self.deprivat(subcommand[0])
        try:
            demiurge.remove_file(filename)
        except NonFileName:
            self.err_stream.write("not file name")

    def echo(self, subcommand: list):
        my_str = " ".join(subcommand)
        if my_str[0] == my_str[-1] == '"':
            my_str = my_str[1:-1]
        self.out_stream.write(my_str)

    def rmdir(self, subcommand: list):
        if not subcommand:
            subcommand.append(self.cur_dir_name)
        elif len(subcommand) != 1 or type(subcommand[0]) is not str:
            self.err_stream.write("too few arguments")
            return

        place = self.deprivat(subcommand[0])
        if path.realpath(place) == path.realpath(self.cur_dir_name):
            self.err_stream.write("you try to delete current directory")
            return
        if path.realpath(place) == path.realpath(self.last_dir):
            self.last_dir = self.cur_dir_name
        try:
            demiurge.remove_directory(place)
        except NonDirName:
            self.err_stream.write("not directory name")
        except InvalidArgument:
            self.err_stream.write("directory is not empty")

    def position(self):
        user = "\033[32m{0}@{1}".format(os.getlogin(), os.uname().nodename)
        cwd = "\033[34m" + self.cur_dir_name_short()
        ans = user + "\033[37m:" + cwd + "\033[37m$"
        return ans

    def mkdir(self, subcommand):
        if not subcommand:
            subcommand[0] = self.cur_dir_name
        elif len(subcommand) != 1:
            self.err_stream.write("incorrect number of arguments")
            return

        output = self.deprivat(subcommand[0])
        try:
            demiurge.make_directory(output)
        except NonDirName:
            self.err_stream.write("incorrect output path")
        except InvalidSyntax:
            self.err_stream.write("incorrect syntax")

    def pwd(self):
        self.out_stream.write(self.cur_dir_name)

    def execute(self, command: str):
        command_place = re.search(r"\$\(.*\)", command)
        while command_place != None:
            subterm = Terminal(FictiveStream(), FictiveStream())
            subcommand_str = command_place.group()
            subcommand_str = subcommand_str[2:-1]
            subterm.execute(subcommand_str)
            result = subterm.out_stream.toString()
            result = '"' + result + '"'
            segment = command_place.span()
            command_new = command[:segment[0]]
            command_new += result
            command_new += command[segment[1]:]
            command = command_new
            command_place = re.search(r'\$\(.*\)', command)

        command = self.parse(command)
        if command[0] == []:
            self.out_stream.write("\r")
        elif command[0][0] == "cd":
            command[0].pop(0)
            self.chdir(command[0])
        elif command[0][0] == "ls":
            command[0].pop(0)
            self.listdir(command[0])
        elif command[0][0] == "cp":
            command[0].pop(0)
            self.copy(command[0])
        elif command[0][0] == "mv":
            command[0].pop(0)
            self.move(command[0])
        elif command[0][0] == "echo":
            command[0].pop(0)
            self.echo(command[0])
        elif command[0][0] == "rm":
            command[0].pop(0)
            self.remove_file(command[0])
        elif command[0][0] == "mkdir":
            command[0].pop(0)
            self.mkdir(command[0])
        elif command[0][0] == "rmdir":
            command[0].pop(0)
            self.rmdir(command[0])
        elif command[0][0] == "pwd":
            self.pwd()
        else:
            self.err_stream.write("what?!?!?!?!?")

    def parse(self, input_command):
        com_non_parsed = input_command.split("|")
        c_size = len(com_non_parsed)
        commands = list()
        for subcom in range(c_size):
            string_swaping = com_non_parsed[subcom].split('"')
            if len(string_swaping) % 2 == 0:
                raise InvalidSyntax
            string_swaping = list(filter(lambda x: x != '', string_swaping))
            commands.append([])
            for i in range(0, len(string_swaping)):
                if i % 2 == 0:
                    c_filter = filter(lambda x: x != '', string_swaping[i].split(r" "))
                    commands[subcom] += list(c_filter)
                else:
                    commands[subcom] += [string_swaping[i]]

        return commands


a = Terminal()
print()
while True:
    try:
        print()
        print(a.position(), end="")
        command = input()
        a.execute(command)

    except KeyboardInterrupt:
        print("\nI remember what you did to me")
        exit()
