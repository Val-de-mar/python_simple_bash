import os
import sys
from executer import Executer
import executer
from time import sleep
import re
from os import path


class FictiveStream:
    def __init__(self):
        self.list_str = []

    def write(self, *args):
        self.list_str += [' '.join(args)]

    def clear(self):
        self.list_str = []

    def read(self, joint="\n"):
        return joint.join(self.list_str)


demiurge = executer.Executer()


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
        flags = []
        for part in enumerate(subcommand):
            if part[1][0] == "-" and len(part[1]) != 1:
                flags += list(part[1])
                flags.remove("-")
                subcommand.pop(part[0])

        if not subcommand:
            subcommand.append(self.cur_dir_name)
        elif len(subcommand) != 1 or type(subcommand[0]) is not str:
            self.err_stream.write("too few arguments")
            return

        place = self.deprivat(subcommand[0])
        try:
            self.out_stream.write(demiurge.listdir(place, "".join(flags)))
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

    def remove_file(self, subcommand: list):
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

    def xargs(self, subcommand: list, instream):
        empty_stream = FictiveStream()
        self.run(subcommand + [instream.read()], empty_stream)

    def cat(self, subcommand: list):
        if len(subcommand) != 1:
            self.err_stream.write("incorrect number of arguments")
        filename = self.deprivat(subcommand[0])
        try:
            self.out_stream.write(demiurge.cat(filename))
        except NonFileName:
            self.err_stream.write("not file name")

    def touch(self, subcommand: list):
        if len(subcommand) != 1:
            self.err_stream.write("incorrect number of arguments")
        filename = self.deprivat(subcommand[0])
        try:
            demiurge.touch(filename)
        except InvalidArgument:
            self.err_stream.write("file already exist")
        except InvalidDir:
            self.err_stream.write("directory doesn't exist")

    def run(self, command: list, in_stream):
        if command == []:
            self.out_stream.write("\r")
        elif command[0] == "cd":
            command.pop(0)
            self.chdir(command)
        elif command[0] == "ls":
            command.pop(0)
            self.listdir(command)
        elif command[0] == "cp":
            command.pop(0)
            self.copy(command)
        elif command[0] == "mv":
            command.pop(0)
            self.move(command)
        elif command[0] == "echo":
            command.pop(0)
            self.echo(command)
        elif command[0] == "rm":
            command.pop(0)
            self.remove_file(command)
        elif command[0] == "mkdir":
            command.pop(0)
            self.mkdir(command)
        elif command[0] == "rmdir":
            command.pop(0)
            self.rmdir(command)
        elif command[0] == "pwd":
            self.pwd()
        elif command[0] == "xargs":
            command.pop(0)
            self.xargs(command, in_stream)
        elif command[0] == "cat":
            command.pop(0)
            self.cat(command)
        elif command[0] == "touch":
            command.pop(0)
            self.touch(command)
        else:
            for i in command:
                self.out_stream.write(i)

    def parseClear(self, command: list, begin: int, in_stream):
        ans = []
        ans.append("")
        end = begin
        i = 0
        escape_char = False
        dollar_is_prev = False
        size = len(command)
        while end < size:
            char = command[end]
            if dollar_is_prev:
                if char == '(':
                    end += 1
                    inter_stream = FictiveStream()
                    empty_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseBrackets(command, end, empty_stream)
                    if ans[i] != "":
                        i += 1
                    else:
                        ans.append("")
                    ans[i] = inter_stream.read()
                    i += 1
                    ans.append("")
                    end = contin - 1
                else:
                    ans[i] += '$'
                    end -= 1
                dollar_is_prev = False
            elif escape_char:
                ans[i] += char
                escape_char = False
            else:
                if char == '\\':
                    escape_char = True
                elif char == '$':
                    dollar_is_prev = True
                elif char == " ":
                    i += 1
                    ans.append("")
                elif char == '"':
                    end += 1
                    inter_stream = FictiveStream()
                    empty_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseDoubleQuotes(command, end, empty_stream)
                    if ans[i] != "":
                        i += 1
                    else:
                        ans.append("")
                    ans[i] = inter_stream.read()
                    i += 1
                    ans.append("")
                    end = contin - 1
                elif char == "'":
                    end += 1
                    inter_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseQuotes(command, end)
                    if ans[i] != "":
                        i += 1
                    ans[i] = inter_stream.read()
                    i += 1
                    end = contin - 1
                elif char == "|":
                    end += 1
                    inter_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    ans = list(filter(lambda x: x != '', ans))
                    inter.run(ans, in_stream)
                    in_stream = inter.out_stream
                    ans = [""]
                    i = 0
                elif char == ")":
                    raise SyntaxError
                else:
                    ans[i] += char

            end += 1
        ans = list(filter(lambda x: x != '', ans))
        self.run(ans, in_stream)
        return end

    def parseDoubleQuotes(self, command: list, begin: int, in_stream) -> int:
        ans = ""
        end = begin
        escape_char = False
        dollar_is_prev = False
        size = len(command)
        while end < size:
            char = command[end]
            if dollar_is_prev:
                if char == '(':
                    end += 1
                    inter_stream = FictiveStream()
                    empty_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseBrackets(command, end, empty_stream)
                    ans += inter_stream.read()

                    end = contin - 1
                else:
                    ans += '$'
                    end -= 1
                dollar_is_prev = False
            elif escape_char:
                ans += char
                escape_char = False
            else:
                if char == '\\':
                    escape_char = True
                elif char == '$':
                    dollar_is_prev = True
                elif char == '"':
                    end += 1
                    self.out_stream.write(ans)
                    return end
                else:
                    ans += char

            end += 1
        raise SyntaxError

    def parseQuotes(self, command: list, begin: int) -> int:
        begin += 1
        ans = ""
        end = begin
        for char in command[begin:]:
            if char == "'":
                end += 1
                self.out_stream.write(ans)
                return end
            else:
                ans += char
            end += 1
        raise SyntaxError

    def parseBrackets(self, command: list, begin: int, in_stream) -> int:
        ans = [""]

        end = begin
        i = 0
        escape_char = False
        dollar_is_prev = False
        size = len(command)
        while end < size:
            char = command[end]
            if dollar_is_prev:
                if char == '(':
                    end += 1
                    inter_stream = FictiveStream()
                    empty_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseBrackets(command, end, empty_stream)
                    if ans[i] != "":
                        i += 1
                    else:
                        ans.append("")
                    ans[i] = inter_stream.read()
                    i += 1
                    ans.append("")
                    end = contin - 1
                else:
                    ans[i] += '$'
                    end -= 1
                dollar_is_prev = False
            elif escape_char:
                ans[i] += char
                escape_char = False
            else:
                if char == '\\':
                    escape_char = True
                elif char == '$':
                    dollar_is_prev = True
                elif char == " ":
                    i += 1
                    ans.append("")
                elif char == '"':
                    end += 1
                    inter_stream = FictiveStream()
                    empty_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseDoubleQuotes(command, end, empty_stream)
                    if ans[i] != "":
                        i += 1
                    else:
                        ans.append("")
                    ans[i] = inter_stream.read()
                    i += 1
                    ans.append("")
                    end = contin - 1
                elif char == "'":
                    end += 1
                    inter_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    contin = inter.parseQuotes(command, end)
                    if ans[i] != "":
                        i += 1
                    ans[i] = inter_stream.read()
                    i += 1
                    end = contin - 1
                elif char == "|":
                    end += 1
                    inter_stream = FictiveStream()
                    inter = Terminal(inter_stream, self.err_stream)
                    ans = list(filter(lambda x: x != '', ans))
                    inter.run(ans, in_stream)
                    in_stream = inter.out_stream
                    ans = []
                    i = 0
                elif char == ")":
                    end += 1
                    ans = list(filter(lambda x: x != '', ans))
                    self.run(ans, in_stream)
                    return end
                else:
                    ans[i] += char

            end += 1
        raise SyntaxError

    def parse(self, command: str):
        pre_parsing = list(command)
        empty_stream = FictiveStream
        try:
            self.parseClear(pre_parsing, 0, empty_stream)
        except SyntaxError:
            sys.stderr.write("invalid syntax")


a = Terminal()
print()
while True:
    try:
        print()
        print(a.position(), end="")
        command = input()
        a.parse(command)

    except KeyboardInterrupt:
        print("\nI remember what you did to me")
        exit()
