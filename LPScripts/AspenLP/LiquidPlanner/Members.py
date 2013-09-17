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

class Member(object):

    def __init__(self,memberInfo):

        for key in memberInfo:
            self.__dict__[key] = memberInfo[key]

class Members(object):
    """
    An LPPackage can contain tasks, projects, or other packages.

    """

    def __init__(self,members):

        self.members = []
        self.memberByName = {}

        for member in members:
            m = Member(member)
            name = m.user_name
            self.memberByName[name] = m
            self.members.append(m)

    def member(self,name):
        if self.memberByName.has_key(name):
            return self.memberByName[name]

        return None


# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

