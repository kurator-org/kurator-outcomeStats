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
__version__ = "Conf.py 2016-05-11T22:52:52-0400"
import xlsxwriter
import configparser
import ast
import yaml
class Conf :
    """
    Instances of Conf produce values of arguments for the constructor of class FPA using the configparser package
    """
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read(self.configFile)
        self.validators = ast.literal_eval(self.config.get('DEFAULT','validators'))
        self.outcomes = ast.literal_eval(self.config.get('DEFAULT','outcomes'))
        self.outcome_colors = ast.literal_eval(self.config.get('DEFAULT','outcome_colors'))
        self.workbookName= self.config.get('DEFAULT', 'workbookName')
        self.workbook = xlsxwriter.Workbook(self.workbookName)
        self.dataFileName = self.config.get('DEFAULT', 'data')
        self.formats= {}
        for outcome, color in self.outcome_colors.items():
            self.formats[outcome] =self.workbook.add_format()
            self.formats[outcome].set_bg_color(color)
        self.worksheet = self.workbook.add_worksheet() ### create here?
        self.typography=self.workbook.add_format({'bold': True})


    def getValidators(self): #should return a tuple of validator names
        return self.validators

    def getOutcomes(self): #should return a tuple of outcome names
        return self.outcomes

    
    def getOutcomeColors(self): #should return an OrderedDictionary with keys from outcome names and values integers representing colors from RGB color model expressed as html RGB strings, e.g. '#00FF00'
        return self.outcome_colors

    def getWorkbook(self): #name or object? do we care which?  #full pathname or local?
        return(self.workbook)
    def getWorkbookName(self): #name or object? do we care which?  #full pathname or local?
        return(self.workbookName)
    
    def getWorksheet(self):
        return(self.worksheet)

    def getDataFileName(self):
        return(self.dataFileName)

def main():
    import pprint
    import xlsxwriter
    print ("main")
    configFile = 'stats.ini'
    config = Conf(configFile)
    


    origin1 = [0,0]
    origin2 = [5,0]
    print(configFile, config.getWorkbook(),config.getWorksheet())
    print("validators=",config.getValidators())
    print("outcomes=",config.getOutcomes())
    print("outcome_colors=", config.getOutcomeColors())

if __name__ == "__main__" :
   main()