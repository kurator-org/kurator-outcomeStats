import json
import xlsxwriter
import configparser
import os
from ConfigRAM import ConfigRAM
#from Stats import Stats
import collections
import sys

class FPA:
#   def __init__(self, workbook, worksheet,infile, outfile, configFile, origin1, origin2):
   def __init__(self, workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2):
#   def __init__(self, config):  #config is a filled ConfigRAM object
      self.workbook = workbook
      self.dataFileName = dataFileName
      self.validators = validators
      self.origin1 = origin1
      self.origin2 = origin2
      self.outcome_colors = outcome_colors # a dict
      print(len(validators), len(outcomes))
#      self.dataFileName = '/home/ram/git/kurator-outcomeStats/occurrence_qc.json' #######
#      self.dataFileName = os.getcwd()+'/'+dataFileName
#      self.data=open(dataFileName, encoding='utf-8')
      print("dataFileName=",self.dataFileName, "type=", type(self.dataFileName))
      self.outcomes = outcomes
      with open(self.dataFileName) as data_file:   ############## could be a stream???
                 self.fpAkkaOutput=json.load(data_file)

      self.formats= {}
      for outcome, color in self.outcome_colors.items():
         self.formats[outcome] =self.workbook.add_format()
         self.formats[outcome].set_bg_color(color)
 #     self.worksheet = self.workbook.add_worksheet()  #set in ConfigRAM

      self.maxlength= max(len(s) for s in self.validators)
      self.max1= max(len(s) for s in self.validators)
      self.max2= max(len(t) for t in self.outcomes)
      self.maxlength = max(self.max1,self.max2)
    #  self.fpa = {}
    #  infile = 'occurrence_qc.json' #for now
    #  with open(infile) as data_file:
    #     self.fpa=json.load(data_file)
      self.stats ={}
      for outcome in self.outcomes:
          self.stats[outcome] = 0
      
      self.numRecords = len(self.fpAkkaOutput)

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
          stats[outcome] = 0
      return stats
   
   def initValidatorStats(self,validators, outcomes) :
      stats = {}
      for v in validators :
         stats[v] = self.initStats(outcomes)
      return stats
   
   def updateValidatorStats(self,fpa, stats, record)  :
      data=fpa[record]["Markers"]
   #   print("in updateValidatorStats[",record,"]")
      for data_k, data_v in data.items() :
         for stats_k, stats_v in stats.items() :
            if (stats_k == data_k):
               stats[stats_k][data_v] += 1
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
            v = v/count_f
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
   

   def stats2XLSX(self, workbook, worksheet, formats, origin, outcomes, validators):
#      print("fmts=",type(formats))
      bold = workbook.add_format({'bold': True})
   #   print("stats=",stats)
   #   print("outcomes=", outcomes)
   #   print(origin)
      worksheet.write(origin[0],origin[1],"Validator",bold)
      for k,v in outcomes :
         col=1+origin[1]+outcomes.index(k) #insure order is as in outcomes list
         worksheet.write(origin[0],col, k, bold) #write col header
      self.maxlength= max(len(s) for s in self.validators)
      self.max1= max(len(s) for s in self.validators)
      self.max2= max(len(t) for t in self.outcomes)
      self.maxlength = max(self.max1,self.max2)
      
#      self.stats = self.setStats()
      print("validators=", validators, "outcomes=", outcomes)
      numRows = len(self.validators)
      numCols = len(self.outcomes)
      stats = {}
      row = 1
      col = 1
      print("numRows=",numRows, "numCols=", numCols)
      sys.exit()
      while row < numRows:
         while col < numCols:
            print("row=",row, "col=",col)
#            stats[row][col] = 0.0
            col = col + 1
         row = row + 1
      sys.exit()
      for k, v in stats.items():
         print("key=",k,"val=", v)
         row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
         print("row=",row)
         worksheet.write(row,0,k) #write validator name
         #write data for each validator in its own row
       ##  for outcome, statval in v.items():
       ##     col=1+outcomes.index(outcome) #put cols in order of the outcomes list
  #          print("formats type=", type(formats))
       ##     format = formats.get(outcome)
      ##      print("format=",format, " type=",type(format)) #gives a class, want an instance
#            worksheet.write(row, col, statval,formats.get(outcome))
#            format = format.getFormat(outcome)
        ##    worksheet.write(row, col, statval, format)
   
   
def main():
   import pprint
   import xlsxwriter
#   import Stats
   configFile = 'stats.ini'
   config = ConfigRAM(configFile)
   origin1 = [0,0]
   origin2 = [5,0]

   workbook = config.getWorkbook()
   worksheet = config.getWorksheet()
   dataFileName = config.getDataFileName()
   validators = config.getValidators()
   print("validators=", validators, "type=", type(validators))
   outcomes = config.getOutcomes()
   outcome_colors = config.getOutcomeColors()
  # print(dataFileName,configFile, workbook,worksheet)
   #print(validators)
   print("outcomes=",outcomes)
   #print(outcome_colors)
   fpa = FPA(workbook, worksheet,dataFileName, validators, outcomes, outcome_colors, origin1, origin2)
   
  # print("fpa=", fpa.getValidators(), fpa.getOutcomes(), fpa.getOutcomeColors())
   print("numRecs=",fpa.getNumRecords())
   print("formats=", fpa.getFormats())
   formats = fpa.getFormats()
   fpa.stats2XLSX(workbook, worksheet, formats, origin1, outcomes, validators)
#   stats = Stats(workbook, worksheet, validators, outcomes, origin1)
#   stats.stats2XLSX(workbook,worksheet,formats,origin1,outcomes,validators)
#   r =range(len(outcomes))
#   print(type(r))
#   for col in range(len(outcomes)):
#      print(col)
   workbook.close()
   
if __name__ == "__main__" :
   print("hello")
   main()
