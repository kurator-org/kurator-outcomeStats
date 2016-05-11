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
__version__ = "FPA.py 2016-05-10T12:30:26-0400"

import json
import xlsxwriter
#import configparser
#import os
#import collections
#import sys

class FPA:
   """
   Instances of FPA produce or modify a color-coded xlsx spreadsheet that allows 
      comparisons against different Validators and Validator outcomes.  
   See "Creating Excel files with Python and XlsxWriter" at http://xlsxwriter.readthedocs.io/
   See also http://wiki.datakurator.net/web/FP-Akka_User_Documentation about the source of the data that 
      this application takes data from.
   """

   """
      workbook : an instance of an xlsxwriter.workbook.Workbook. It models an Excel XLSX Workbook

      worksheet : an instance of an xlsxwriter.worksheet.Worksheet. It models an Excel XLSX Worksheet

      dataFileName : a python str providing the name of the output of the FP-Akka workflowstarter.jar as described in
              http://wiki.datakurator.net/web/FP-Akka_User_Documentation. At this writing such a file
              must be JSON. Such a file need not be provided by FP-Akka itself. The workflowstarter jar
              provides more than this FPA class processes, and there will be forthcoming description of what
              such a JSON file must contain at a minimum

      validators : a tuple of validator names mentioned in the dataFile named in dataFileName. 
              A validator is an object that can apply data quality criteria.
              Example provided by  FP-Akka: 
              ('ScientificNameValidator','DateValidator',  'GeoRefValidator','BasisOfRecordValidator') 

      outcomes : a tuple of outcome names mentioned in the dataFile. 
              An outcome is one of a named outputs of a validator
              Example: ('CORRECT','CURATED','FILLED_IN', 'UNABLE_DETERMINE_VALIDITY',  'UNABLE_CURATE') 
              TODO: treat case where not every outcome is meaningful to every validator

      outcome_colors : a dictionary keyed by outcome names with values given as HTML RGB colors
              Example: outcome_colors = {'CORRECT':'#00FF00', 'CURATED':'#FFFF00', 'FILLED_IN':'#DDDD00', 'UNABLE_DETERMINE_VALIDITY':'#888888',  'UNABLE_CURATE':'#FF0000' }

      origin1 : a list describing the origin of a location of the first Validator by Outcome table in the worksheet
              Example: [0,0]
      origin2 : a list describing the origin of a location of a second Validator by Outcome table in the worksheet
              Example: [5,0]
              Typically there might be two tables, one at top of the spreadsheet, and a second below it positioned
              1+len(validators) below the first.  In such a use, the first set would have total outcome count in
              each entry and second set would normalize by the total number of records in the dataFile. 
              See setCells(...) below

   
   """
   def __init__(self, workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2):
      thing = origin2
#      print("thing=",thing, "type=", type(thing))
      self.workbook = workbook
      self.dataFileName = dataFileName
      self.validators = validators
      self.origin1 = origin1
      self.origin2 = origin2
      self.outcome_colors = outcome_colors # a dict
      self.outcomes = outcomes
      with open(self.dataFileName) as data_file:   ############## could be a stream???
                self.data= self.fpAkkaOutput=json.load(data_file)

      self.formats= {}
      for outcome, color in self.outcome_colors.items():
         self.formats[outcome] =self.workbook.add_format()
         format = workbook.add_format()

      self.maxlength= max(len(s) for s in self.validators)
      self.max1= max(len(s) for s in self.validators)
      self.max2= max(len(t) for t in self.outcomes)
      self.maxlength = max(self.max1,self.max2)

      self.stats ={}
      for outcome in self.outcomes:
         self.stats[outcome] = 0
#          self.stats[outcome] = repr(0)
#          print("type: ", type(self.stats[outcome]))
      self.numRecords = len(self.fpAkkaOutput)

   def normalizeStats(self, stats, norm):
      """ divide every outcome value by norm """
      import copy
      statsNormed = copy.deepcopy(stats)
#      print('statsNormed=',statsNormed)
      for validator,stat in statsNormed.items():
#         print("stat=",stat)
         for outcome, value in stat.items():
#            print("value=",value, "type=", type(value))
            valueNew = value/norm
#            print("valueNew",valueNew, "type=", type(valueNew))
            stat[outcome] = valueNew
#      print('statsNormed=',statsNormed)
      return statsNormed
      
   def setCells(self, workbook, worksheet, stats, origin, validators, outcomes,outcome_colors, normalize):
      """
         stats is a dictionary with validator names as keys and dictionaries as values. The value dictionaries
            have outcomes as keys and a number as value; when normalize = False, that number is an integer 
            that is the number of records having the given outcome for the given validator.
            If normalize = True, then this stat value is a float which is the corresponding number divided
            by the number of  data records processed by stats2XLSX(...) 

         cell colors are set from outcome_colors
         
         excel numeric formats are hard coded here as either '0.000' if normalize = True or else default,
            which is normally as an integer.  Possibly the numeric format should be an argument

         NOTE: subsequent worksheet.write(...) can change the worksheet
      """
      thing = stats
#      print("in setCells thing=",thing, "type=", type(thing))
      for k, v in stats.items():
         row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
         worksheet.write(row,0,k) #write validator name

         #write data for each validator in its own row
         for outcome, statval in v.items():
            col=1+outcomes.index(outcome) #put cols in order of the outcomes list
            if normalize:
               format= workbook.add_format({'bg_color': outcome_colors[outcome], 'num_format': '0.000'})
               stat = statval/self.getNumRecords()
            else:
               format= workbook.add_format({'bg_color': outcome_colors[outcome]})
               stat = statval
            worksheet.write(row, col, stat, format) #set appropriate cell with value stat 

   def getStats(stats) :
      return self.stats
   def getOutcomes(self) :
      return self.outcomes
   def getValidators(self) :
      return self.validators
   def getMaxLength(self):
      return self.maxlength
   def getOutcomeColors(self) :
      return self.outcome_colors
   def getNumRecords(self):
      return self.numRecords
   def getFormats(self):
      return self.formats
   
   def initStats(self,outcomes) :  #to do: insure only called once at FPA instantiation 
      stats = {}
      for outcome in outcomes:
          stats[outcome] = float(0)
      return stats
   
   def initValidatorStats(self,validators, outcomes) :  #to do: insure only called once at FPA instantiation 
      stats = {}
      for v in validators :
         stats[v] = self.initStats(outcomes)
      return stats
   
   def updateValidatorStats(self,fpa, stats, record)  :
      data=fpa[record]["Markers"]
#      print("in updateValidatorStats[",record,"]")
      for data_k, data_v in data.items() :
         for stats_k, stats_v in stats.items() :
            if (stats_k == data_k):
               stats[stats_k][data_v] += 1.0
      return stats
   
   def stats2CSV(self, stats, outfile, outcomes, validators):
      import csv
      with open(outfile, 'w') as csvfile:
         o=outcomes
         o.insert(0,"Validator")
         fieldnames=tuple(o)
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
         writer.writeheader()
         for v in validators:
            row = stats[v]
            row['Validator'] = v
            writer.writerow(row)
   

   def stats2XLSX(self, workbook, worksheet, formats, origin, outcomes, validators):  #to do: are multiple calls OK?
      """
      Function produces a stats dictionary whose keys are validator names and whose values are dictionaries that,
         in turn have keys that are outcome names and values are a number that is a statistic for the given outcome.
         An example is shown in setCells(...)
      """
      bold = workbook.add_format({'bold': True}) #for col headers
 
         #Set col headers
      worksheet.write(origin[0],origin[1],"Validator",bold) 
      for outcome in outcomes:
         col=1+origin[1]+outcomes.index(outcome) #insure order is as in outcomes list
         worksheet.write(origin[0],col, outcome, bold) #write col header
         colWidth = len(outcome)*2   #heuristic compromise
         worksheet.set_column(origin[0],col, colWidth)

         #Set row names
      for k in validators:
         row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
         worksheet.write(row,0,k) #write validator name

      self.max1 =      max(len(s) for s in self.validators)
#      self.maxlength = max(len(s) for s in self.validators)
      self.maxlength = self.max1
      self.max2 = max(len(t) for t in self.outcomes)
      self.maxlength =  max(self.max1,self.max2)
      
         #initialize stats for accumulation over records
      numRows = len(self.validators)
      numCols = len(self.outcomes)
      stats = [[0.0 for x in range(numCols)] for y in range(numRows)]
      row = 1
      col = 1

      ###fill stats from FPA object

      self.fpa = self.data
#      print("len(fpa)=",len(self.fpa))
      validatorStats = self.initValidatorStats(self.validators, self.getOutcomes())
      for record in range(len(self.fpa)):
         validatorStats = self.updateValidatorStats(self.fpa, validatorStats, record)
##         if normalize == True :
##            self.normalizeStats(self.fpa,validatorStats)
      return validatorStats
             
   
   
def main():
   """Example"""
   from Conf import Conf
   import pprint
   import xlsxwriter

   configFile = 'stats.ini'
   config = Conf(configFile)
   origin1 = [0,0]
   origin2 = [5,0]

   workbook = config.getWorkbook()
   worksheet = config.getWorksheet()
   dataFileName = config.getDataFileName()
  # print("dataFileName=", dataFileName())
   validators = config.getValidators()

   outcomes = config.getOutcomes()
   outcome_colors = config.getOutcomeColors()

   fpa = FPA(workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2)
   
   formats = fpa.getFormats()
   stats=fpa.stats2XLSX(workbook, worksheet, formats, origin1, outcomes, validators)
   fpa.setCells(workbook, worksheet, stats, origin1, validators, outcomes, outcome_colors,False)
  # stats=fpa.stats2XLSX(workbook, worksheet, formats, origin2, outcomes, validators)
   stats2=fpa.normalizeStats(stats, fpa.getNumRecords())
   fpa.setCells(workbook, worksheet, stats2, origin2, validators, outcomes, outcome_colors,False)

   workbook.close()
   
if __name__ == "__main__" :
   main()