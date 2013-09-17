#!usr/bin/python
#
# This is an example of how to use the LiquidPlanner API in Python.
#

# You need the Requests library, found at:
# http://docs.python-requests.org/en/latest/index.html
#
import requests

import json
import getpass

class Base(object):

    buildDef = {
    }

    def __init__(self,parent,treeItem):
        self.item = treeItem
        self.parent = parent
        self.name = treeItem['name']
        self.id= treeItem['id']

        self.packages = []
        self.projects = []
        self.folders = []
        self.tasks = []

    def insertProject(self,obj):
        self.projects.append(obj)

    def insertPackage(self,obj):
        self.packages.append(obj)

    def insertFolder(self,obj):
        self.folders.append(obj)

    def insertTask(self,obj):
        self.tasks.append(obj)

    def __str__(self):
        return "Name:%s" % self.item['name']


# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

