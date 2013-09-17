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

class PackageTree(Base):
    """
    An LPPackage can contain tasks, projects, or other packages.

    """

    def __init__(self,parent,treeItem):
        super(Package,self).__init__(parent,treeItem)

        if not treeItem['is_done']:
            parent.insertPackage(self)

            if treeItem.has_key('children'):
                for treeItem in treeItem['children']:
                    cls = Base.buildDef[treeItem['type']]
                    obj = cls(self,treeItem)

class Package(object):

    def __init__(self,memberInfo):

        for key in memberInfo:
            self.__dict__[key] = memberInfo[key]

    def has_key(self,key):
        return self.__dict__.has_key(key)


# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

