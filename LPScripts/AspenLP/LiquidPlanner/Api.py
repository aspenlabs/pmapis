#!usr/bin/python
#
# This is an example of how to use the LiquidPlanner API in Python.
#

# You need the Requests library, found at:
# http://docs.python-requests.org/en/latest/index.html
#
import requests


from time import sleep
import json
from urllib import quote
from Members import  Members
from Projects import Projects
from Folder import Folder, Folders
from Package import *
from Packages import *

class ApiCore(object):
    """
    Implement the low-level LiquidPlanner API

    This class uses the requests library to send GET, PUT and POST requests to the
    REst API.

    The urllib.quote function is used to quote special characters in filters.

    This class implements the core API functions PUT, GET, and POST

    """

    base_uri = 'https://app.liquidplanner.com/api'

    def __init__(self, email, password):
        """
        Initialize the session. Must pass in the user id and e-mail required
        to connect to the LiquidPlanner API
        """

        self.email    = email
        self.password = password
        # set default headers for all requests made with this session:
        self.session = requests.Session()

        self.session.auth = (self.email, self.password)
        self.session.headers['content-type'] = 'application/json'

        self.reqinfo = {
            'headers' : {'content-type': 'application/json'},
            'auth' : (self.email, self.password)
        }

        self.options = {
            "headers": {'Content-Type': 'application/json'},
            "auth" : (self.email,self.password)
        }

    def getWorkspaceId(self):
        return self.workspace_id
    
    def setWorkspaceId(self, workspace_id):
        self.workspace_id = workspace_id
  
    def get(self, uri, options={}):
        """
        Low level GET routine that uses the pre-configured session to send a get request.
        The get data is normally included in the URI
        """
        return self.session.get(self.base_uri + uri, data=options)
    
    def post(self, uri, options={}):
        """
        Low level POST routine that uses the pre-configured session to send a POST request,
        along with post data.
        """
        return self.session.post(self.base_uri + uri, data=options)
    
    def put(self, uri, options={}):
        """
        Low level PUT routine that uses the pre-configured session to send a PUT request,
        along with PUT data.
        """
        return self.session.put(self.base_uri + uri, data=options)

    def jget(self,path):
        """
        Call the get routine and convert the results to a json data structure.
        """
        s = self.get(path).content
        return json.loads(s)

    def jpost(self,uri,options={}):
        """
        Call the post routine and convert the results to a json data structure.
        """
        s = self.post(uri,options).content
        return json.loads(s)

    def jput(self,uri,options={}):
        """
        Call the put routine and convert the results to a json data structure.
        """
        s = self.put(uri,options).content
        return json.loads(s)


class Api(ApiCore):
    """
    Implement the High or Mid Level LiquidPlanner functions, using the ApiCore as a base
    class.
    """

    def __init__(self,email,password):
        super(Api,self).__init__(email,password)

    def getAccount(self):
        """
        Returns a dictionary with information about the current user
        """
        return self.jget('/account')

    def getWorkspaces(self):
        """
        Returns a list of dictionaries, each a workspace in which this user is a member
        """
        return self.jget('/workspaces')

    def getFirstWorkspace(self):
        """
        Returns a list of dictionaries, each a workspace in which this user is a member
        """
        workSpaces = self.jget('/workspaces')
        if len(workSpaces) == 0:
            raise Exception("No valid workspaces were returned.")

        return workSpaces[0]

    def ws(self):
        """
        Shortcut routine to return the leading portion of the URI with the selected workspace ID
        """
        return "/workspaces/%d/" % self.workspace_id

    def getFilteredObjects(self,key,**kwargs):
        """
        Query an API list endpoint with a filter.
        """
        filters = []
        params = []

        for arg in kwargs:
            if arg == 'filters' and kwargs['filters']:
                filters = kwargs['filters']
            if arg == 'params' and kwargs['params']:
                params = kwargs['params']

        uri = self.ws()+key

        query = []

        for param in params:
            query.append("%s" % quote(param))

        for filter in filters:
            query.append("filter[]=%s" % quote(filter))

        uri += "?" + "&".join(query)
        print("Query URI:%s" % uri)
        return self.jget(uri)

    def getFolders(self,**kwargs):
        """
        Returns a list of dictionaries, each a project in a workspace
        """

        p = self.getFilteredObjects('folders',**kwargs)
        return Folders(p)

    def getProjects(self,**kwargs):
        """
        Returns a list of dictionaries, each a project in a workspace
        """

        p = self.getFilteredObjects('projects',**kwargs)
        return Projects(p)

    def getPackages(self,**kwargs):
        """
        Returns a list of dictionaries, each a project in a workspace
        """
        p = self.getFilteredObjects('packages',**kwargs)
        return Packages(p)

    def getMembers(self):
        """
        Return a list of members for this workspace.
        """
        m = self.jget(self.ws() + 'members')
        return Members(m)

    def getTasks(self,**kwargs):
        """
        Returns a list of dictionaries, each a task in a workspace.

        The optional 'filters' parameter is a list of filters that are used to
        filter the tasks on the server side.

        """
        filters = []

        for arg in kwargs:
            if arg == 'filters' and kwargs['filters']:
                filters = kwargs['filters']

        uri = self.ws()+'tasks'

        query = []

        for filter in filters:
            query.append("filter[]=%s" % quote(filter))

        uri += "?" + "&".join(query)
        return self.jget(uri)

    def getTaskById(self,id,**kwargs):
        """
        Returns a list of dictionaries, each a task in a workspace.

        The optional 'filters' parameter is a list of filters that are used to
        filter the tasks on the server side.

        """
        filters = []

        for arg in kwargs:
            if arg == 'filters' and kwargs['filters']:
                filters = kwargs['filters']

        uri = self.ws()+'tasks/%d' % id

        query = []

        for filter in filters:
            query.append("filter[]=%s" % quote(filter))

        uri += "?" + "&".join(query)
        return self.jget(uri)

    def getTaskDataById(self,id,key,**kwargs):
        """
        Returns a list of dictionaries, each a task in a workspace.

        The optional 'filters' parameter is a list of filters that are used to
        filter the tasks on the server side.

        """
        filters = []

        for arg in kwargs:
            if arg == 'filters' and kwargs['filters']:
                filters = kwargs['filters']

        uri = self.ws()+'tasks/%d/%s' % (id,key)

        query = []

        for filter in filters:
            query.append("filter[]=%s" % quote(filter))

        uri += "?" + "&".join(query)
        return self.jget(uri)

    def updateTask(self,taskid,**kwargs):
        """
        Update the given task id, using the arguments in kwargs.

        Usage: obj.updateTask(taskId,owner_id=12345, is_done=true, ...)
        """

        uri = self.ws() + 'tasks/%d' % taskid

        optionstring = json.dumps({'task' : kwargs})
        return self.put(uri,optionstring)

    def createTask(self, data):
        """
        Creates a task by POSTing data
        """
        optionstring = json.dumps({'task': data})
        res = self.jpost(self.ws()+'tasks',optionstring)
        return res

    def addChecklistItems(self,taskid,checklist):
        """
        Add a list of checklist items to the given task id.
        """
        uri = self.ws() + 'tasks/%d/checklist_items' % taskid
        for cl in checklist:
            optionstring = json.dumps({'checklist_item' : cl})
            self.jpost(uri,optionstring)
            sleep(0.5)


    def treeItems(self,**kwargs):
        """
        List all tree items with the given depth. The default depth is -1, returning
        all items.
        """

        depth = -1
        filters = []

        for arg in kwargs:
            if arg == 'depth':
                depth = kwargs['depth']

        uri = self.ws()+'treeitems'
        if depth >= 0:
            uri += "?depth=%d" % depth
        else:
            uri += "?depth=-1&leaves=true"

        return self.jget(uri)

    def treeItemsById(self,id,**kwargs):
        """
        List all tree items with the given depth. The default depth is -1, returning
        all items.
        """

        depth = -1
        filters = []

        for arg in kwargs:
            if arg == 'depth':
                depth = kwargs['depth']

        uri = self.ws()+'treeitems/%d' % id
        if depth >= 0:
            uri += "?depth=%d" % depth
        else:
            uri += "?depth=-1&leaves=true"

        return self.jget(uri)

# invoke the demo, if you run this file from the command line
if __name__ == '__main__':
    Api.task()

