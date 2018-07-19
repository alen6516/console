#!/usr/bin/python
# -*- coding: utf-8 -*-
#####
# File Name: main.py
# Author: alen6516
# Created Time: 2018-06-11
#####

# base cmd exception
class CmdException(Exception):
    """ exception when user give a wrong para to a command """

    def __init__(self, msg):
        super(CmdException, self).__init__()
        self.msg = msg
    
# base cmd
class Cmd(object):
        
    cmd_dict = {}

    @classmethod
    def parser(cls, cmd_name, para_list):
        if cmd_name in cls.cmd_dict.keys():
            cls.cmd_dict[cmd_name].handler(para_list)

        else:
            print("no such command, use help to show avaliable commands")

    @classmethod
    def reg(cls, cmd_name, cmd):
        cls.cmd_dict[cmd_name] = cmd

    
    def __init__(self, name):
        self.name = name
        self.info = "this is the help of command %s" % self.name
        

    def handler(self, para_list):
        """ main para parsing handler """
        
        try:
            if "--help" in para_list or "-h" in para_list:
                print(self.info)
    
            else:
                self._handler(para_list)
        
        except CmdException as e:
            
            print("command error")
            print(e.msg)

        except KeyboardInterrupt as e:
            print("")


    def _handler(self, para_list):
        """ cusmized para parsing handler """
        pass


class Help(Cmd):
    def __init__(self):
        super(Help, self).__init__("help")
        self.info = "show the avaliable commands in this console"

    def _handler(self, para_list):
        if para_list:
            raise CmdException(msg="%s does not require any para" % self.name)
        
        else:
            for cmd_name, instance in self.cmd_dict.items():
                print("%s\t%s" % (cmd_name, instance.info))
    
class Exit(Cmd):
    def __init__(self):
        super(Exit, self).__init__("exit")
        self.info = "exit this console"

    def _handler(self, para_list):
        if para_list:
            raise CmdException(msg="%s does not require any para" % self.name)
        
        else:
            import sys
            sys.exit(0)


class Count(Cmd):
    def __init__(self):
        super(Count, self).__init__('count')
        self.info = "count a number"

    def _handler(self, para_list):
        if not para_list:
            raise CmdException(msg="please give a int")
        
        elif len(para_list) > 1:
            raise CmdException(msg="please give only one int")

        else:
            try:
                num = int(para_list[0])
                import time              
 
                for i in range(num, 0, -1):
                    print(i)
                    time.sleep(1)
                           
            except ValueError as e:
                print("please give an integer")


def init():
    Cmd.reg("help", Help())
    Cmd.reg("exit", Exit())
    Cmd.reg("count", Count())


def cut_line(line):

    re = line.split(' ')
    cmd = re[0]
    para_list = re[1:]
    return cmd, para_list


def main():

    init()
    print("use help to check avaliable command")
    
    try:
        while True:
            line = raw_input("console >>> ")
        
            line = " ".join(line.split())   # remove duplicate space
        
            if line == '':
                continue

            cmd, para_list = cut_line(line)
            Cmd.parser(cmd, para_list)
    
    except (KeyboardInterrupt, EOFError) as e:
        print("exit")
        
main()        
