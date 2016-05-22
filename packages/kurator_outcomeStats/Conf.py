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
__version__ = "Conf.py 2016-05-20T22:15:26-0400"
import xlsxwriter
import ConfigParser
import ast
#import yaml
import xlsxwriter
from ConfigParser import SafeConfigParser
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


def main():
    import ConfigParser
    print ("main")
    parser = ConfigParser.ConfigParser()
    print (parser)
    rx = parser.read('./stats.ini')
    print  ("rx=",rx)
#    configFile = 'stats.ini'
#    config = Conf(configFile)
#    sx = config.sections()
    sx = parser.get('DEFAULT',  'origin1')
    print ("sx=",sx)
    #print (config.options('DEFAULT'))
    
    


if __name__ == "__main__" :
   main()
