#!/usr/bin/env python

import sys
import os, os.path
from path import path
import argparse
import re

from AspenLP.AspenLP import AspenLP
from AspenLP.FileProcessor import FileProcessor

import pickle

class EEWebLPProject(AspenLP):
    """
    Iterate over lib dir, find all .js files, then create test stubs
    for files that don't have them.
    """

    def __init__(self):
        super(EEWebLPProject,self).__init__()

    def processLine(self,line):
        """
        Iterate over the patterns, if any match, perform the replacement
        """

        function = None
        m = re.search("^\w+\.prototype\.(\w+)\s*=\s*",line)
        if m:
            function = m.group(1)

        return function

    def processFile(self,file):
        """

        """

        functions = []

        #print("Processing %s" % file)

        # Now, copy the file and process it.
        prefix = os.path.basename(file)

        fp = open(file,'r')

        for line in fp:
            function = self.processLine(line)
            if function:
                functions.append(function)

        fp.close()
        return functions

    def buildTask(self,filename,functions):
        """
        Use the list of functions, and a template to build the test stub
        """

        estimate = 1 + 0.2*len(functions)
        low = 0.8*estimate
        hi = 1.2 *estimate

        taskName = "Assess %s tests,UnitTestTeam,%f - %f" % (filename,low,hi)

        return taskName



def main():
    """
    Main driver for the script.

    """

    parser = argparse.ArgumentParser(description="generateTestStubs")

    parser.add_argument("taskFile",
                        help="Path for assignment file.")

    args = parser.parse_args()

    if not os.path.exists(args.taskFile):
        print("Task file does not exist.")
        sys.exit(1)

    taskMgr = EEWebLPProject()
    taskMgr.initLP()

    #taskMgr.listProjects()
    #taskMgr.loadTree(["project_id=8008922"])
    tasks = taskMgr.getTasks(["project_id=6890048"],parent_id=8008922)

    fileByAssignee = taskMgr.getTaskOwners(args.taskFile)
    taskMgr.updateTaskOwners(fileByAssignee,tasks)

if __name__ == '__main__':
    main()
