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

class Task(Base):
    """
    An LPTask is the lowest item in the list.
    """

    def __init__(self,parent,treeItem):
        super(Task,self).__init__(parent,treeItem)
        if not treeItem['is_done']:
            parent.insertTask(self)
            for key in treeItem:
                self.__dict__[key] = treeItem[key]

class SimpleTask(object):

    def __init__(self,task):

        for key in task:
            self.__dict__[key] = task[key]

# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

