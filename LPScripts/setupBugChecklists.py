#!/usr/bin/env python

import argparse

from AspenLP.AspenLP import *

import pickle

class BugChecklists(AspenLP):
    """
    Iterate over lib dir, find all .js files, then create test stubs
    for files that don't have them.
    """

    checklistItems = [
        'Review/Assign, Ed',
        'Verify Bug',
        'Commit Fix',
        'Verify Fix, Partsim Tester'
    ]


    def __init__(self):
        super(BugChecklists,self).__init__()

    def updateProject(self,proj,lvl=0,path=""):
        """
        Update project level stuffs..
        """

        if not proj.has_key('children'):
            print("No children for %s" % proj['name'])
            return

        print("Updating tasks for %s" % path)

        for child in proj['children']:
            t = child['type']
            if t == 'Task':
                checkList = self.lp.getTaskDataById(child['id'],'checklist_items')
                for item in checkList:
                    print("Item name " + item['name'])

                pass

            elif t == 'Folder':
                self.updateProject(child,lvl+1,path + ":" + child['name'])


    def updateAllChecklists(self,topPkg):
        """
        This is so complex, I'm making some great simplifications to start with.
        topPkg is the 'Product Releases' package.
        topPkg.children is a list of projects
            * ignore anything not a project.
            - each project contains a list of folders
                * ignore anything not a folder
                * one of the folders will contains 'Bugs'
                - 'Bugs' folder contains a list of folders and tasks.
                    - iterate into folders for additional tasks.
                    - for each task
                        - get the checklist
                            - if the checklist is empty, fill with the default
                            - if the checklist is not empty..... do something smart

        """

        for child in topPkg['children']:
            t = child['type']
            print ("Child type %s" % child['type'])
            if t == 'Project':
                self.updateProject(child,0,child['name'])


def main():
    """
    Main driver for the script.

    """

    parser = argparse.ArgumentParser(description="setupBugChecklist")

    #parser.add_argument("rootpath",
    #                    help="Path for bug dir.")

    args = parser.parse_args()

    lp = BugChecklists()
    lp.initLP()

    webapps = lp.getPackage(filters=['name = Webapps'])

    #webapps_all = lp.getPackages(filters=['name = Webapps'], params=['depth=-1','include_children=all','leaves=true'])

    f = 'owner_id = %d' % webapps.id
    relpkg = lp.getPackage(filters=['name contains Releases'])

    relpkg_items = lp.getTreeItemsById(relpkg.id,params=['include_children=all','leaves=true'])

    lp.updateAllChecklists(relpkg_items)

    print("Done")

if __name__ == '__main__':
    main()
