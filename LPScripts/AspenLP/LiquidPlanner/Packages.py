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

from Package import Package

class Packages(object):
    """
    An LPPackage can contain tasks, projects, or other packages.

    """

    def __init__(self,pkgList):

        self.packages = []
        self.packagesByName = {}

        for pkg in pkgList:
            m = Package(pkg)
            name = m.name
            self.packagesByName[name] = m
            self.packages.append(m)

    def package(self,name):
        if self.packagesByName.has_key(name):
            return self.packagesByName[name]

        return None

    def __iter__(self):
        return iter(self.packages)


# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    pass

