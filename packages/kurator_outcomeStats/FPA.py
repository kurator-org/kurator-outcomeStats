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
__version__ = "FPA 2016-06-11T12:23:26-0400"

import json
import xlsxwriter
#from OPT import OPT
import argparse
import logging
from dwca_utils import response
from dwca_utils import setup_actor_logging


def FPA(options):
   """Build options to prepare 
   options - a dictionary of parameters
      outputfile - - name of xlsx workbook file
      worksheetName - optional name of worksheet in output file
      inputfile - name of inputfile usually a JSON file with QC data for each record
      validators - list of validator names
      outcomes - list of outcome names
       outcome_colors : a dictionary keyed by outcome names with values given as HTML RGB colors
              Example: outcome_colors = {'CORRECT':'#00FF00', 'CURATED':'#FFFF00', 'FILLED_IN':'#DDDD00', 'UNABLE_DETERMINE_VALIDITY':'#888888',  'UNABLE_CURATE':'#FF0000' }

      origin1 : a list describing the origin of a location of the first Validator by Outcome table in the worksheet
   Example: [0,0]
      origin2 : a list describing the origin of a location of a second Validator by Outcome table in the worksheet
              Example: [5,0]
              Typically there might be two tables, one at top of the spreadsheet, and a second below it positioned with the same column headers
              1+len(validators) below the first.  In such a use, the first set would have total outcome count in
              each entry and second set would normalize by the total number of records in the dataFile. 
      workspace - path to a directory for the outputfile
      success - True if process completed successfully, otherwise False
      message - an explanation of the reason if success=False
      artifacts - a dictionary of persistent objects created
      """
   setup_actor_logging(options)

   logging.debug( 'Started %s' % __version__ )
   logging.debug( 'options: %s' % options )

        # Make a list for the response
   returnvars = ['workspace', 'inputfile', 'outputfile', 'worksheet', 'formats', 'origin', 'outcomes', 'validators', 'success', 'message', 'artifacts']

        # Make a dictionary for artifacts left behind
   artifacts = {}

       # outputs
   success = False
   message = None

       # inputs
   try:
      workspace = options['workspace']
   except:
      workspace = None

   if workspace is None or len(workspace)==0:
      workspace = './'

   try:
      outputfile = options['outputfile']
   except:
      outputfile = None
   if outputfile is None or len(outputfile)==0:
      outputfile='qcstats.xlsx'
        
   print("In FPA")

def _getoptions():
    """Parse command line options and return them."""
    parser = argparse.ArgumentParser()

    help = 'Name  of the file from which to read QC records (required)'
    parser.add_argument("-i", "--inputfile", help=help)

    help = 'directory for the output file (optional)'
    parser.add_argument("-w", "--workspace", help=help)

    help = 'output xlsx file name, no path (optional)'
    parser.add_argument("-ws", "--worksheetname", help=help)

    help = 'optional name of worksheet in output file'
    parser.add_argument("-o", "--outputfile", help=help)
    
    help = 'log level (e.g., DEBUG, WARNING, INFO) (optional)'
    parser.add_argument("-l", "--loglevel", help=help)

    parser.add_argument("-oc","--outcomes", nargs="+")
    
    return parser.parse_args()
   
   
##   def getOpt(self):
##      return(self.opt)
   

#   def f3(opt.get('workbook'), opt.get('worksheet'), opt.get('dataFileName'), opt.get('validators'), opt.get('outcomes'), opt.get('outcome_colors'), opt.get('origin1',default=None), opt.get('origin2',default=None))

def __init4__(self, workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2):
   self.optionsList = list({workbook,worksheet, dataFileName, validators, outcomes})#, outcome_colors, origin1, origin2}
   self.optionsList.append(outcome_colors)
   self.optionsList.append(origin1)
   self.optionsList.append(origin2)
   a = ['workbook', workbook, 'outcomes',outcomes,'dataFileName',dataFileName,'worksheet', worksheet,'outcome_colors', outcome_colors,'origin1',origin1,'origin2',origin2,'validators',validators]
   self.options = {item : a[index+1] for index, item in enumerate(a) if index % 2 == 0}
   thing = self.options
#   print("thing=",thing, "type=", type(thing))
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
      self.numRecords = len(self.fpAkkaOutput)

   def getOptions(self):
      return self.options
   
   def normalizeStats(self, stats, norm):
      """ divide every outcome value by norm and return a new stats object. """
      import copy
      statsNormed = copy.deepcopy(stats)
      for validator,stat in statsNormed.items():
         for outcome, value in stat.items():
            valueNew = value/norm
            stat[outcome] = valueNew
      return statsNormed

   def stats2XLSX(self, workbook, worksheet, formats, origin, outcomes, validators):  #to do: are multiple calls OK?
      """
      Function produces a stats dictionary whose keys are validator names and whose values are dictionaries that,
         in turn have keys that are outcome names and values are a number that is a statistic for the given outcome.
      Although the returned stats object has the statistic data filled in, it is NOT written to the worksheet. That can be done by the setCells(...) function
      
         An example is shown in setCells(...)
      """
      bold = workbook.add_format({'bold': True}) #for col headers
      wrap = workbook.add_format()
      wrap.set_text_wrap()
 #     header_format = {'bold': True, 'text_wrap':True}
      header_format= wrap
         #Set col headers
      worksheet.write(origin[0],origin[1],"Validator",bold) 
      for outcome in outcomes:
         col=1+origin[1]+outcomes.index(outcome) #insure order is as in outcomes list
#         worksheet.write(origin[0],col, outcome, bold) #write col header
#         print("wrap=",wrap)
         colWidth = len(outcome)*2   #heuristic compromise
#         worksheet.set_column(origin[0],col, colWidth)
#         worksheet.set_column(origin[0],col,10,wrap)
#         worksheet.set_column(origin[0],col,wrap)
         worksheet.set_column('B:F', 10, wrap) #TODO locate by origin, replace "10" by param
         bold.set_text_wrap() #do both bold and textwrap formats
         worksheet.write(origin[0],col, outcome, bold) #write col header


         #Set row headers from validator names
      for k in validators:
         row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
         worksheet.write(row,0,k) #write validator name

         #get sizes for column width TODO: get the column where the actual placment will be
      self.max1 =      max(len(s) for s in self.validators)
#      self.maxlength = max(len(s) for s in self.validators)
      worksheet.set_column('A:A', self.max1)
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
      validatorStats = self.initValidatorStats(self.validators, self.getOutcomes())
      for record in range(len(self.fpa)):
         validatorStats = self.updateValidatorStats(self.fpa, validatorStats, record)
      return validatorStats
      
   def setCells(self, workbook, worksheet, stats, origin, validators, outcomes, outcome_colors,format, normalize):
      """
         stats is a dictionary with validator names as keys and dictionaries as values. The value dictionaries
            have outcomes as keys and a number as value; when normalize = False, that number is an integer 
            that is the number of records having the given outcome for the given validator.
            
         cell colors are set from outcome_colors
         
         excel numeric formats are hard coded here as either '0.000' if normalize = True or else default,
            which is normally as an integer.  Possibly the numeric format should be an argument

         NOTE: subsequent worksheet.write(...) can change the worksheet
      """
#      self.normalize = normalize
#      thing = numeric_format
      self.normalize = normalize
#      thing = numeric_format
#      print(thing)
#      print("in setCells thing=",thing, "type=", type(thing))

#      self.numeric_format = numeric_format
      for k, v in stats.items():
         row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
         worksheet.write(row,0,k) #write validator name

         #write data for each validator in its own row
         if self.normalize == False:
            numeric_format = '0' #only ints
         else:
            numeric_format = '0.00%'
         for outcome, statval in v.items():
            col=1+outcomes.index(outcome) #put cols in order of the outcomes list
            format= workbook.add_format({'bg_color': outcome_colors[outcome], 'num_format':numeric_format })
            stat = statval
            worksheet.write(row, col, stat, format) #set appropriate cell with value stat 

   def getStats(self) :
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
   def getWorkbook(self):
      return self.workbook
   
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
      for data_k, data_v in data.items() :
         for stats_k, stats_v in stats.items() :
            if (stats_k == data_k):
               stats[stats_k][data_v] += 1.0
      return stats
   
   def stats2CSV(self, stats, outfile, outcomes, validators): #BUG: requires a complete stats object
      """
      This function assumes that the stats dictionary has meaningful and complete statistics. But in
      turn that may only happen i, e.g., FPA.stats2XLSX() has run and then stats produced by FPA.getStats()
      """
      import csv
      import copy
      with open(outfile, 'w') as csvfile:
#         o=copy.deepcopy(outcomes)
         o = list(outcomes)
         o.insert(0,"Validator")
         fieldnames=tuple(o)
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
         writer.writeheader()
         for v in validators:
            row = stats[v]
            row['Validator'] = v
            writer.writerow(row)
   

   
def main():
   options = _getoptions()
   optdict = {}

   if options.inputfile is None or len(options.inputfile)==0:
      s = 'syntax:\n'
      s += 'python FPA.py'
      s += ' -i ./data/occurrence_qc.json'
      s += ' -o ./data/outcomeStats.xlsx'
      s += ' -ws .qc_stats'
      s += ' -oc outcomes'
      s += ' -w ./workspace'
      s += ' -l DEBUG'
      print '%s' % s
      return

   optdict['inputfile'] = options.inputfile
   optdict['outputfile'] = options.outputfile
   optdict['worksheetname'] = options.worksheetname
   optdict['outcomes'] = options.outcomes
   optdict['workspace'] = options.workspace
   optdict['loglevel'] = options.loglevel
   print 'optdict: %s' % optdict

   response = FPA(optdict)
   print '\nresponse: %s' % response
  #### return



   """Example"""
#   from OPT import OPT
 ###  from FPA import FPA
###   import pprint
###   import xlsxwriter

   configFile = 'stats.ini'
###   opt = OPT(configFile)
   #here get the options
#   fpa = FPA(workbook, workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2)
###   fpa = FPA(opt)
   origin1 = [0,0]
   origin2 = [5,0]

##   workbook = fpa.getWorkbook()
##   worksheet = fpa.getWorksheet()
##   dataFileName = opt.getDataFileName()
  # print("dataFileName=", dataFileName())
##   validators = opt.getValidators()
   

###   outcomes = opt.getOutcomes()
###   outcome_colors = opt.getOutcomeColors()

###   fpa = FPA(workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2)
   
###   formats = fpa.getFormats()
###   stats=fpa.stats2XLSX(workbook, worksheet, formats, origin1, outcomes, validators)
###   fpa.setCells(workbook, worksheet, stats, origin1, validators, outcomes, outcome_colors)
####   stats=stats2XLSX(workbook, worksheet, formats, origin2, outcomes, validators)
####   print ("stats=",stats)
###   stats2=fpa.normalizeStats(stats, fpa.getNumRecords())
###   cell_numeric_format = '0.00' 
###   fpa.setCells(workbook, worksheet, stats2, origin2, validators, outcomes, outcome_colors, cell_numeric_format)
###   validators=fpa.getValidators()
###   print("validators=",validators, type(validators))
###   fpa.stats2CSV(stats,"stats.csv", outcomes,validators)

###   workbook.close()

if __name__ == "__main__" :
   main()
   print("version=", __version__)

