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
from Base import Base


class Folder(Base):

    def __init__(self,parent,treeItem):
        super(Folder,self).__init__(parent,treeItem)

        if not treeItem['is_done']:
            parent.insertFolder(self)

            if treeItem.has_key('children'):
                for treeItem in treeItem['children']:
                    cls = Base.buildDef[treeItem['type']]
                    obj = cls(self,treeItem)

class SimpleFolder(object):

    def __init__(self,folder):
        super(SimpleFolder,self).__init__()

        for key in folder:
            self.__dict__[key] = folder[key]


class Folders(object):
    """
    An LPPackage can contain tasks, projects, or other packages.

    """

    def __init__(self,folderList):

        self.folders = []
        self.foldersByName = {}

        for fldr in folderList:
            m = SimpleFolder(fldr)
            name = m.name
            self.foldersByName[name] = m
            self.folders.append(m)

    def folder(self,name):
        if self.foldersByName.has_key(name):
            return self.foldersByName[name]

        return None

    def __getitem__(self,idx):

        try:
            return self.folders[idx]
        except:
            return None

# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

