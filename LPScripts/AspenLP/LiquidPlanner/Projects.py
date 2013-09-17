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

class Project(object):

    def __init__(self,memberInfo):

        for key in memberInfo:
            self.__dict__[key] = memberInfo[key]

class Projects(object):
    """
    An LPPackage can contain tasks, projects, or other packages.

    """

    def __init__(self,projList):

        self.projects = []
        self.projectsByName = {}

        for proj in projList:
            m = Project(proj)
            name = m.name
            self.projectsByName[name] = m
            self.projects.append(m)

    def project(self,name):
        if self.projectsByName.has_key(name):
            return self.projectsByName[name]

        return None


# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

