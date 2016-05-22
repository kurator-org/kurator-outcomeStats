#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Robert A. Morris"
__copyright__ = "Copyright 2016 President and Fellows of Harvard College"
__version__ = "Options.py 2016-05-22T18:14:56-0400"
import xlsxwriter
import ConfigParser
import ast
#import yaml
import xlsxwriter
from ConfigParser import SafeConfigParser
import ast
#import yaml
class Options :
    """
    Instances of Conf produce values of arguments for the constructor of class FPA using the configparser package
    """
    def __init__(self, configFile):
        self.configFile = configFile
        self.parser = SafeConfigParser()
#        self.config = configparser.ConfigParser()
#        self.config.sections()
        self.parser.read(self.configFile)
        self.validators = ast.literal_eval(self.parser.get('DEFAULT','validators'))
#        print (self.validators)
        self.outcomes = ast.literal_eval(self.parser.get('DEFAULT','outcomes'))
        self.outcome_colors = ast.literal_eval(self.parser.get('DEFAULT','outcome_colors'))
        self.workbookName= self.parser.get('DEFAULT', 'workbookName')
        self.workbook = xlsxwriter.Workbook(self.workbookName)
        self.dataFileName = self.parser.get('DEFAULT', 'dataFileName')
        self.formats= {}
        for outcome, color in self.outcome_colors.items():
            self.formats[outcome] =self.workbook.add_format()
            self.formats[outcome].set_bg_color(color)
        self.worksheet = self.workbook.add_worksheet() ### create here?
        self.typography=self.workbook.add_format({'bold': True})
        self.origin1 = ast.literal_eval(self.parser.get('DEFAULT', 'origin1'))
        self.origin2 = ast.literal_eval(self.parser.get('DEFAULT', 'origin2'))

    def getParser(self):
        return self.parser

    def getOutcomes(self):
        return self.outcomes
    def getOutcomeColors(self):
        return self.outcome_colors
    
    def getValidators(self):
        return self.validators

    def getWorkbookName(self): #name or object? do we care which?  #full pathname or local?
        return self.WorkbookName
    def getWorkbook(self): #name or object? do we care which?  #full pathname or local?
        return self.workbook

    def getFormats(self):
        return self.formats
    
    def getWorksheetName(self):
        return self.worksheetName
    def getWorksheet(self):
        return self.worksheet
    
    def getDataFileName(self):
        return self.dataFileName

    def getOrigin1(self):
        return self.origin1
    def getOrigin2(self):
        return self.origin2
def main():
    options = Options('./stats.ini')
    parser = options.getParser()
    print (parser.get('DEFAULT','outcome_colors'))
    print (parser.get('DEFAULT','outcomes'))
#    import ConfigParser
#    print ("main")
#    parser = ConfigParser.ConfigParser()
#    print (parser)
#    rx = parser.read('./stats.ini')
#    print  ("rx=",rx)
#    configFile = 'stats.ini'
#    config = Conf(configFile)
#    sx = parser.sections()
#    sx = parser.get('DEFAULT',  'origin1')
#    print ("sx=",sx)
    #print (parser.options('DEFAULT'))
    
    


if __name__ == "__main__" :
   main()
