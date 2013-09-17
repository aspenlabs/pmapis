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



class Project(Base):
    """
    An LPProject contains project sub-folders and tasks.
    Project sub-folders may be may be nested to any depth
    """

    def __init__(self,parent,treeItem):
        super(Project,self).__init__(parent,treeItem)

        if not treeItem['is_done']:
            parent.insertProject(self)

            if treeItem.has_key('children'):
                for treeItem in treeItem['children']:
                    cls = Base.buildDef[treeItem['type']]
                    obj = cls(self,treeItem)


# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

