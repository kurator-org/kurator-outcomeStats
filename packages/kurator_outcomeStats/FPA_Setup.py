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
__version__ = "FPA_Setup.py 2016-05-17T18:18:59-0400"

import json
import copy
import xlsxwriter
"""
#{'worksheet': <xlsxwriter.worksheet.Worksheet object at 0x7fb224519748>, 'workbook': <xlsxwriter.workbook.Workbook object at 0x7fb2245194e0>, 'outcome_colors': {'CORRECT': '#00FF00', 'UNABLE_CURATE': '#FF0000', 'FILLED_IN': '#DDDD00', 'CURATED': '#FFFF00', 'UNABLE_DETERMINE_VALIDITY': '#888888'}, 'dataFileName': 'occurrence_qc.json', 'origin1': [0, 0], 'outcomes': ('CORRECT', 'CURATED', 'FILLED_IN', 'UNABLE_DETERMINE_VALIDITY', 'UNABLE_CURATE'), 'origin2': [5, 0]
, 'validators': ('ScientificNameValidator', 'DateValidator', 'GeoRefValidator', 'BasisOfRecordValidator')}
"""
def xlsx_setup(setup):
   """
This function takes a dictionary of options of the form
inputDict={'worksheetName': 'qc_stats', 'workbookName': 'outcomeStats.xlsx', 'outcome_colors': {'CORRECT': '#00FF00', 'UNABLE_CURATE': '#FF0000', 'FILLED_IN': '#DDDD00', 'CURATED': '#FFFF00', 'UNABLE_DETERMINE_VALIDITY': '#888888'}, 'dataFileName': 'occurrence_qc.json', 'origin1': [0, 0], 'outcomes': ('CORRECT', 'CURATED', 'FILLED_IN', 'UNABLE_DETERMINE_VALIDITY', 'UNABLE_CURATE'), 'origin2': [5, 0], 'validators': ('ScientificNameValidator', 'DateValidator', 'GeoRefValidator', 'BasisOfRecordValidator')}

and returns one of the form
outputDict={'outcome_colors': {'CURATED': '#FFFF00', 'CORRECT': '#00FF00', 'UNABLE_CURATE': '#FF0000', 'FILLED_IN': '#DDDD00', 'UNABLE_DETERMINE_VALIDITY': '#888888'}, 'outcomes': ('CORRECT', 'CURATED', 'FILLED_IN', 'UNABLE_DETERMINE_VALIDITY', 'UNABLE_CURATE'), 'worksheet': <xlsxwriter.worksheet.Worksheet object at 0x7f9362e556d8>, 'workbook': <xlsxwriter.workbook.Workbook object at 0x7f93644c3908>, 'origin2': [5, 0], 'origin1': [0, 0], 'dataFileName': 'occurrence_qc.json', 'validators': ('ScientificNameValidator', 'DateValidator', 'GeoRefValidator', 'BasisOfRecordValidator')} 

But note the corresponding k,v pairs in the output may not be in the same order in the output as in the input

It might be  that a python generator is a more general approach than done here
   """
   xlsxSetup = copy.deepcopy(setup) #prepare a copy

      # replace key 'workbookName' with key 'workbook'
   xlsxSetup['workbook'] = xlsxSetup.pop('workbookName') 
   workbook  = xlsxwriter.Workbook(setup.get('workbookName')) #build workbook model 
   xlsxSetup['workbook'] = workbook #set value as workbook
      # similarly set up 'worksheet' k,v pair
   worksheet =  workbook.add_worksheet(setup.get('worksheetName'))  # worksheet with default name
   xlsxSetup['worksheet'] = xlsxSetup.pop('worksheetName')
   xlsxSetup['worksheet'] = worksheet  #set value as worksheet
   thing = xlsxSetup
   print("in FP_Setup thing=",thing, "type=", type(thing))
   return xlsxSetup
   



   
   
def main():
   """Example"""
   setup = { 'workbookName': 'outcomeStats.xlsx', 'worksheetName': 'qc_stats','outcome_colors': {'CORRECT': '#00FF00', 'UNABLE_CURATE': '#FF0000', 'FILLED_IN': '#DDDD00', 'CURATED': '#FFFF00', 'UNABLE_DETERMINE_VALIDITY': '#888888'}, 'dataFileName': 'occurrence_qc.json', 'origin1': [0, 0], 'outcomes': ('CORRECT', 'CURATED', 'FILLED_IN', 'UNABLE_DETERMINE_VALIDITY', 'UNABLE_CURATE'), 'origin2': [5, 0], 'validators': ('ScientificNameValidator', 'DateValidator', 'GeoRefValidator', 'BasisOfRecordValidator')}
   fpopts = xlsx_setup(setup)
  # print("fpopts=", fpopts)
if __name__ == "__main__" :
   main()
   print("version=", __version__)

