



class FileProcessor(object):

    def __init__(self):

        pass

    @staticmethod
    def fileContainsPattern(file,pattern):
        """
        Open a file, and search to see if the file contains the
        given pattern. If it does, then return the groups from
        that pattern
        """

        fp = open(file,'r')
        pat = re.compile(pattern)
        for line in fp:
            m = pat.search(line)
            if m:
                fp.close()
                return True

        fp.close()
        return False

    def processLine(self,line):
        """
        Iterate over the patterns, if any match, perform the replacement
        """

        function = None
        m = re.search("^\w+\.prototype\.(\w+)\s*=\s*",line)
        if m:
            function = m.group(1)

        return function

    def processFile(self,file):
        """

        """

        functions = []

        #print("Processing %s" % file)

        # Now, copy the file and process it.
        prefix = os.path.basename(file)

        fp = open(file,'r')

        for line in fp:
            function = self.processLine(line)
            if function:
                functions.append(function)

        fp.close()
        return functions

