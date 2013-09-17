
import os
import re


from LiquidPlanner.Api import Api
from LiquidPlanner.Root import Root
from LiquidPlanner.Task import SimpleTask
from LiquidPlanner.Members import Members

import liquidplanner

class AspenLP(object):

    def __init__(self):
        self.ws_id = 65698

        loginInfo = "~/.liquidlogin"
        if os.path.exists(os.path.expanduser(loginInfo)):
            self.loadLoginInfo(os.path.expanduser(loginInfo))
        else:
            print("Please create a ~/.liquidlogin file")
            sys.exit(2)

        self.lpapi = liquidplanner.LiquidPlanner(self.email,self.password)
        self.lp = Api(self.email,self.password)

        self.lp.setWorkspaceId(self.workspace_id)

        self.workspace = None
        self.members = None
        self.projects = None

    def initLP(self):

        if not self.workspace:
            self.workspace = self.lp.getFirstWorkspace()
            self.lp.setWorkspaceId(self.workspace['id'])

    def loadLoginInfo(self, file):
        """
        Store the LiquidPlaner login information in a
        user file in your home directory:
        Filename: ~/.liquidlogin

        Contents:
        email:<your e-mail address>
        password:<your lp password>
        workspace:65698
        """

        fp = open(file,"r")
        for line in fp:
            m = re.search("((email|password|workspace):(.*))",line)
            if m:
                if m.group(2) == 'email':
                    self.email = m.group(3)
                if m.group(2) == 'password':
                    self.password = m.group(3)
                if m.group(2) == 'workspace':
                    self.workspace_id = m.group(3)

        fp.close()

    def loadProjects(self):

        self.projects = self.lp.getProjects()

    def loadMembers(self):

        self.members = self.lp.getMembers()

    def listProjects(self):

        self.initLP()
        print "Here is a list of all of your projects:"
        for project in self.projects:
            path = project['parent_crumbs']
            path.append(project['name'])
            projPath = ":".join(path)
            print("Project ID:%d Path:%s" % (project['id'],projPath))

    def kwFilter(self,objects,**kwargs):
        """
        Reulable keyword argument filter, for filtering a list of
        objects by some parameter.
        """

        if kwargs and kwargs.has_key('postfilter'):
            filtered = []
            for arg in kwargs['postfilter']:
                val = kwargs[arg]
                for obj in objects:
                    if obj.has_key(arg) and obj[arg] == val:
                        filtered.append(obj)

            return filtered

        return objects

    def getMembers(self,**kwargs):
        objects = self.lp.getMembers()

        return objects

    def getTasks(self,**kwargs):

        objects = self.lp.getTasks(**kwargs)

        return self.kwFilter(objects,**kwargs)

    def getFolders(self,**kwargs):

        objects = self.lp.getFolders(**kwargs)

        return self.kwFilter(objects,**kwargs)

    def getProjects(self,**kwargs):

        objects = self.lp.getProjects(**kwargs)

        return self.kwFilter(objects,**kwargs)

    def getPackages(self,**kwargs):

        objects = self.lp.getPackages(**kwargs)

        return self.kwFilter(objects,**kwargs)

    def getPackage(self,**kwargs):

        p = self.getPackages(**kwargs)

        if len(p.packages) == 1:
            return p.packages[0]

        return None

    def getPackageItems(self,pkg,**kwargs):

        p = self.lp.getFilteredObjects('packages/%d' % pkg.id,**kwargs)
        return p

    def getTreeItems(self,filters = None):

        treeItems = None
        pickleFile = '/tmp/lptree.pcl'

        if not filters and os.path.exists(pickleFile):
            fp = open(pickleFile,'r')
            treeItems = pickle.load(fp)
            fp.close()

        else:
            if filters:
                treeItems = self.lp.treeItems(filters=filters)
            else:
                treeItems = self.lp.treeItems()

            fp = open(pickleFile,'w')
            pickle.dump(treeItems,fp)
            fp.close()

        return treeItems

    def getTreeItemsById(self,id,**kwargs):

        return self.lp.treeItemsById(id,**kwargs)

    def loadTree(self,filters=None):
        tree = self.getTreeItems(filters)

        if tree['type'] == 'Root':
            cls = Root(tree)
            return cls

    def getProject(self,project):
        project_id = 0
        return project_id

    def addTask(self,project,taskInfo):

        print "Adding a new task to your first project..."
        project_id = self.getproject(project)
        new_task = self.lp.createTask({"name":"learn the API","parent_id":int(project_id)})
        print "Added task %(name)s with id %(id)s" % new_task

    def addChecklistItems(self,taskid,checklist):
        """
        Add a list of checklist items to the given task id.
        """
        return self.lp.addChecklistItems(taskid, checklist)

    def createTask(self,taskInfo):

        res = self.lp.createTask(taskInfo)
        return SimpleTask(res)

    def getTaskOwners(self,taskfile):

        fp = open(taskfile,'r')

        currentAssignee = None
        fileAssignments = {}
        fileByAssignee = {}

        for line in fp:
            m = re.search("Assigned:(\w+)",line)
            if m:
                currentAssignee = m.group(1)
                if not fileByAssignee.has_key(currentAssignee):
                    fileByAssignee[currentAssignee] = []

            m = re.search("(eeLib/.*/.*\.js)",line)
            if m:
                currFile = m.group(1)
                if currentAssignee:
                    fileAssignments[currFile] = currentAssignee
                    fileByAssignee[currentAssignee].append(currFile)


        fp.close()

        return fileByAssignee

    def updateTaskOwners(self,fileByAssignee,tasks):

        # Parse tasks into a dictionary
        taskDict = {}
        for task in tasks:
            m = re.match("Assess (\w+) tests",task['name'],re.I)
            if m:
                taskFile = m.group(1)
                taskDict[taskFile] = task

        for assignee in fileByAssignee:
            m = self.members.member(assignee)
            if not m:
                print("Member %s not found" % assignee)
            else:
                assignments = fileByAssignee[assignee]
                for assignment in assignments:
                    taskName = os.path.splitext(os.path.basename(assignment))[0]
                    if taskDict.has_key(taskName):
                        task = taskDict[taskName]
                        if task['owner_id'] != m.id:
                            out = self.lp.updateTask(task['id'],owner_id=m.id)
                            print("Task \"%s\" assigned to user %s" % (task['name'],assignee))
                        else:
                            print("Task \"%s\" already assigned to user %s" % (task['name'],assignee))

