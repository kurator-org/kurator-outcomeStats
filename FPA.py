import json
import xlsxwriter
import configparser
import os
from Conf import Conf
import collections
import sys

class FPA:
   def __init__(self, workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2):
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

   def showFormat(self,theFormat):
      print("showFormat")
      
   def setCells(self, workbook, worksheet, stats, origin, validators, outcomes,outcome_colors, normalize):
      print("in setCells numRec=", self.getNumRecords())
      for k, v in stats.items():
         row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
         worksheet.write(row,0,k) #write validator name

         #write data for each validator in its own row
         for outcome, statval in v.items():
            col=1+outcomes.index(outcome) #put cols in order of the outcomes list
            format = workbook.add_format()
            format.set_bg_color(outcome_colors[outcome])
            if normalize: 
               stat = statval/self.getNumRecords()
            else:
               stat = statval
            worksheet.write(row, col, stat, format)

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
   
   def initStats(self,outcomes) :
      stats = {}
      for outcome in outcomes:
          stats[outcome] = float(0)
      return stats
   
   def initValidatorStats(self,validators, outcomes) :
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
#               x=float(stats[stats_k][data_v])
#               x += 1
               stats[stats_k][data_v] += 1.0
#               stats[stats_k][data_v] = repr(x)
      return stats
   
   #typed parameter requires python3
   def createStats(self, fpa, normalize):
      validatorStats = self.initValidatorStats(self.validators, self.outcomes)
      for record in range(len(fpa)):
         self.updateValidatorStats(fpa, validatorStats, record) 
      if normalize == True :
         self.normalizeStats(fpa,validatorStats)
      return validatorStats
   
   def normalizeStats(self,fpa,stats):
      #fpa is dict loaded from FP-Akka json output
      #divide outcome counts by occurrence counts
      count=len(fpa)
      count_f= float(count)
   #   if (count <= 0) return(-1)
      for validator,outcomes in stats.items():
         stat=stats[validator]
         for k,v in stat.items():
            v = float(v)/count_f
            stat[k] = format(v, '.4f')
   #         print("yy:",stats[validator])
   #   print("in normalize stats=",stats)
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
   
   def initWorkbook(outfile):
      """
      Returns a workbook to be written to **outfile**
      """
      workbook = xlsxwriter.Workbook(outfile)
      return workbook
   

   def stats2XLSX(self, workbook, worksheet, formats, origin, outcomes, validators, normalize):

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
  ##    normalize = False ###for now
      print("len(fpa)=",len(self.fpa))
      validatorStats = self.initValidatorStats(self.validators, self.getOutcomes())
      for record in range(len(self.fpa)):
         validatorStats = self.updateValidatorStats(self.fpa, validatorStats, record)
         if normalize == True :
            self.normalizeStats(self.fpa,validatorStats)
      return validatorStats
             
   
   
def main():
   import pprint
   import xlsxwriter
   configFile = 'stats.ini'
   config = Conf(configFile)
   origin1 = [0,0]
   origin2 = [5,0]

   workbook = config.getWorkbook()
   worksheet = config.getWorksheet()
   dataFileName = config.getDataFileName()
   validators = config.getValidators()

   outcomes = config.getOutcomes()
   outcome_colors = config.getOutcomeColors()

   fpa = FPA(workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2)
   
   formats = fpa.getFormats()
   stats=fpa.stats2XLSX(workbook, worksheet, formats, origin1, outcomes, validators,False)
   fpa.setCells(workbook, worksheet, stats, origin1, validators, outcomes, outcome_colors,False)
   stats=fpa.stats2XLSX(workbook, worksheet, formats, origin2, outcomes, validators, False)
   fpa.setCells(workbook, worksheet, stats, origin2, validators, outcomes, outcome_colors,True)

   workbook.close()
   
if __name__ == "__main__" :
   main()
