#!/usr/bin/env python

import argparse
import sys
import os,os.path
from time import sleep

from AspenLP.AspenLP import *
from AspenLabs.ExcelFile import CachedExcelFile

class SpiceModelProject(AspenLP):
    """
    Iterate over lib dir, find all .js files, then create test stubs
    for files that don't have them.
    """

    checklistItems = [
        'Develop',
        'Review, Ed',
    ]


    def __init__(self):
        super(SpiceModelProject,self).__init__()


    def getProjectid(self):
        """
        Get the project id of the "Maxim-IC Model LIbrary"
        project, and then the ID of the 'ModelLibrary' project sub-folder
        """



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

class ModelFiles(CachedExcelFile):

    def __init__(self):
        super(ModelFiles,self).__init__('/tmp/spicemodels.dat')

    def importExcel(self,xlfile):
        """
        Import the excel file that contains the spice models.

        """

        data = self.loadFromCache(xlfile)

        if data:
            return data

        self.printmsg("Importing Excel file %s" % xlfile,1)
        wb = self.openWorkbook(xlfile)

        if not wb:
            return

        sheetName = self.getSheets()[0]
        if sheetName == None:
            self.printmsg("Components worksheet not found in %s" % xlfile,1)

        ws = self.getSheet(sheetName)

        nrows = self.getRowCount(ws)
        print("Total number of Main rows is %d" % nrows)
        ncols = self.getColumnCount(ws)
        if ncols > self.maxCols:
            print("We have a problem with this sheet. Total columns is %d" % ncols)
            return []

        rowHeadings = self.getValues(ws,0)

        if len(rowHeadings) > 100:
            print("Dang - something is very wrong, we have %d row headings!!" % len(rowHeadings))
            return []

        # Find the column that contains the models
        modelCol = None
        col = 0
        for hdg in rowHeadings:
            m = re.search('Model',hdg)
            if m:
                modelCol = col
                break

            col += 1

        allModels = {}

        for rowid in range(1,nrows):
            self.currRow = rowid
            if rowid % 100 == 0:
                print("Processing row %d" % rowid)
            theRow = self.getValues(ws,rowid)
            mdl = theRow[modelCol]
            if mdl != '':
                allModels[mdl] = rowid

        data = sorted(allModels.keys())
        self.saveToCache(data)
        return data


def main():
    """
    Main driver for the script.

    """

    parser = argparse.ArgumentParser(description="buildModelTasks")

    parser.add_argument('xlfile',
                        help="XLFile with tasks in it")

    #parser.add_argument("rootpath",
    #                    help="Path for bug dir.")

    args = parser.parse_args()

    models = ModelFiles()
    spiceModels = models.importExcel(args.xlfile)

    print "There are %d models to create tasks for." % len(spiceModels)

    lp = SpiceModelProject()
    lp.initLP()

    projects = lp.getProjects(filters=['name contains "Model Library"'])
    maximProj = projects.project('Partsim Model Library')

    members = lp.getMembers()

    frank = members.memberByName['Franklin Rey']
    emman = members.memberByName['Emman']
    ed = members.memberByName['Ed']

    modelLibFolder = lp.getFolders(filters=['name contains "ModelLibrary"','project_id = %d' % maximProj.id])[0]
    maximFolders = lp.getFolders(filters=['project_id = %d' % maximProj.id])
    maximTasks = lp.getTasks(filters=['is_done is false','project_id = %d' % maximProj.id])

    #modelLibTasks = lp.getTasks(filters=['is_done is false','parent_id = %d' % modelLibFolder.id])

    checklistItems = [
        { 'name' : 'Define Symbol'},
        { 'name' : 'Test with ngspice'},
        { 'name' : 'Add to Component List'},
        { 'name' : 'Review', 'owner_id' : ed.id }
        ]


    sleep(4)
    ownerIds = [frank.id, emman.id]
    idx = 0
    for model in spiceModels:
        task = "Test and Define Model:%s" % model

        tinfo = {
            'name' : task,
            'project_id' : maximProj.id,
            'parent_id' : modelLibFolder.id,
            'owner_id' : ownerIds[idx%2]
        }

        t = lp.createTask(tinfo)
        sleep(0.5)
        task_id = t.id
        lp.addChecklistItems(task_id,checklistItems)
        idx += 1
        if idx % 10 == 0:
            print("Updated %d tasks" % idx)


    #f = 'owner_id = %d' % webapps.id
    #relpkg = lp.getPackage(filters=['name contains Releases'])

    #relpkg_items = lp.getTreeItemsById(relpkg.id,params=['include_children=all','leaves=true'])

    #lp.updateAllChecklists(relpkg_items)

    print("Done")

if __name__ == '__main__':
    main()
