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
from Project import Project
from Task import Task
from Package import Package
from Folder import Folder
from Event import Event

class Root(Base):
    """
    This is the root class of the tree
    """

    def __init__(self,treeItem):
        super(Root,self).__init__(None,treeItem)

        Base.buildDef = {
            'Inbox'   : Project,
            'Task'    : Task,
            'Package' : Package,
            'Project' : Project,
            'Folder'  : Folder,
            'Event'   : Event
            }

        if treeItem.has_key('children'):
            if not treeItem['is_done']:
                for treeItem in treeItem['children']:
                    cls = Base.buildDef[treeItem['type']]
                    obj = cls(self,treeItem)



# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

