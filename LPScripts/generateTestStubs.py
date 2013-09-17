#!/usr/bin/env python

import sys
import os, os.path
from path import path
import argparse
import re

import shutil
from tempfile import mktemp

class TestStubGen(object):
    """
    Iterate over lib dir, find all .js files, then create test stubs
    for files that don't have them.
    """

    def __init__(self,srcDir,moduleDir):

        if not os.path.isdir(srcDir):
            print("Source directory %s does not exist" % srcDir)

        if not os.path.isdir(moduleDir):
            print("Module directory %s does not exist" % moduleDir)

        self.srcDir = srcDir
        self.moduleDir = moduleDir

    def isScriptGenerated(self,file):

        return self.fileContainsPattern(file,"SCRIPT_GENERATED")


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

    def buildTask(self,filename,functions):
        """
        Use the list of functions, and a template to build the test stub
        """

        estimate = 1 + 0.2*len(functions)
        low = 0.8*estimate
        hi = 1.2 *estimate

        taskName = "Assess %s tests,UnitTestTeam,%f - %f" % (filename,low,hi)

        return taskName


    def buildStub(self,filename,testname,functions):
        """
        """
        str = """

/**
 * Tests for %s object
 * SCRIPT_GENERATED
 */

/**
  * Test Definitions
  * This information is parsed by php to determine what modules to load
  * in the html file. See the specification document for details about
  * what to put here.
  testDefinitions:begin

  #library:<require library>
  #mockup:<any mockups needed from the tests/mockups dir
  mockup:eeApp
  mockup:EEWeb

  # Use default for mockups, eelib and modules that match the test name
  testmockup:*default
  eelib:*default
  module:*default

  html:start
  # HTML For any DOM nodes required for this test.
  html:end

  css:start
  # CSS As needed.

  css:end

  testDefinitions:end
  */

var jsHintOptions = {

    curly: true,
    eqeqeq: true,
    forin: true,
    unused: false,
    debug: true,
    jquery: true,
    undef: false,
    strict: false

};

JsHamcrest.Integration.QUnit();
JsMockito.Integration.QUnit();

QUnit.module('%s', {
    setup: function() {

        EEWeb = getMockEEWeb({
            mockType: 'eeApp',
            eventLog: true,
            eventSource: true
        });

        //may need more initialization here
    },
    teardown: function() {

    }
});


"""  % (testname,testname)

        funcDefs = ""

        for function in functions:
            funcDef = """
test("function %s", function() {

    qHint.validateObject( %s.prototype.%s , jsHintOptions );
    //add assertions to the test
});

""" % (function,testname,function)
            funcDefs += funcDef

        fp = open(filename,'w')
        fp.write(str)
        fp.write(funcDefs)
        fp.close()

    def GenerateStubs(self,overwrite):

        tasks = []

        dir = path(self.srcDir)
        for jsFile in dir.walk("*.js"):
            fileName = os.path.basename(jsFile)
            file,ext = os.path.splitext(fileName)
            testFile = "test_" + file + ".js"
            testName = os.path.join(self.moduleDir,testFile)

            functions = self.processFile(jsFile)
            tasks.append(self.buildTask(file,functions))

            if os.path.exists(testName):
                if overwrite and self.isScriptGenerated(testName):
                    print("Overwriting file %s" % testName)
                    os.unlink(testName)
                    self.buildStub(testName,file,functions)
            else:
                print("Generating new stub file %s" % testName)
                self.buildStub(testName,file,functions)

        fp = open(os.path.join(self.moduleDir,"tasks.txt"),"w")
        for task in tasks:
            fp.write(task+ "\n")

        fp.close()


def main():
    """
    Main driver for the script.

    """

    parser = argparse.ArgumentParser(description="generateTestStubs")

    parser.add_argument("sourcepath",
                        help="Path for .js files.")

    parser.add_argument("modulepath",
                        help="Path for test .js files.")

    parser.add_argument("--overwrite",
        action="store_true",
        help="Overwrite existing files.")

    args = parser.parse_args()

    tsg = TestStubGen(args.sourcepath, args.modulepath)

    tsg.GenerateStubs(args.overwrite)


if __name__ == '__main__':
    main()
