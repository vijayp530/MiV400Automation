__author__ = 'mkr'

import os
import re

class Reader:
    def __init__(self, logger):
        self.logger = logger
        self.logger.debug("Begin")
        self.logger.debug("End")

    def get_commands(self, command_file):
        self.logger.debug("Begin")
        commands = []
        if os.path.exists(command_file):
            with open(command_file) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not (line == '' or re.match('^#', line)):
                        commands.append(line)
        self.logger.debug("End")
        return commands

    def format_commands(self, commands):
        self.logger.debug('Begin')
        maincommandlist = []
        linecount = 0
        subdict = {}
        isthread = False
        for cmd in commands:
            cmd=cmd.split()
            if isthread == False:
                if re.search(r'thread', cmd[0].lower()):
                    linecount = int(cmd[1])
                    isthread = True
                else:
                    #not a thread create dictionary and append to main list
                    subdict[cmd[0]]=[" ".join(cmd[1:])]
                    maincommandlist.append(subdict)
                    subdict={}
            else:
                #add line to dict
                if cmd[0] in subdict.keys():
                    subdict[cmd[0]].append(" ".join(cmd[1:]))
                else:
                    subdict[cmd[0]]=[" ".join(cmd[1:])]
                linecount = linecount - 1
                if linecount == 0:
                    #add the sub dictionary to list
                    maincommandlist.append(subdict)
                    isthread = False
                    subdict={}
            self.logger.debug('Begin')
            return maincommandlist