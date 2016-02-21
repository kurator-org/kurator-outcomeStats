import json
import sys
import xlsxwriter
import argparse
from OutcomeStats import *
class OutcomeFormats:
   """Class supporting xlsx cell formats for a set of Kurator Quality Control *outcomes*
   """
   def __init__(self, outcomes):
      self.outcomes = outcomes
      
   def getFormats(self):
      return formats

   def setFormats(self, formats):
      return {}
   
   def initFormats(self, workbook):
      formatGrnFill=workbook.add_format()
      formatRedFill=workbook.add_format()
      formatYelFill=workbook.add_format()
      formatMusFill=workbook.add_format()
      formatGryFill=workbook.add_format()
      formatGrnFill.set_bg_color('#00FF00') #lite green
      formatRedFill.set_bg_color('#FF0000')
      formatMusFill.set_bg_color('#DDDD00') #mustard
      formatYelFill.set_bg_color('#FFFF00')
      formatGryFill.set_bg_color('#888888')
      formatXFill=''
      self.formats={'UNABLE_DETERMINE_VALIDITY':formatGryFill, 'CURATED':formatYelFill, 'UNABLE_CURATE':formatRedFill, 'CORRECT':formatGrnFill, 'FILLED_IN':formatMusFill}
      return self.formats

def main():
   print("OutcomeFormats.main()")
#   print(type(self.outcomeFormats()))

if __name__ == "__main__" :
   print("hello")
   main()
parser = argparse.ArgumentParser()
parser.add_argument('--i',default='occurrence_qc.json', help="Defaults to occurrence_qc.json if '--i' absent")
parser.add_argument('--o',default='outcomeStats.xlsx', help="Defaults to outcomeStats.xlsx if '--o' absent")
parser.add_argument('--c',default='stats.ini', help="Defaults to stats.ini if --c absent")
args = parser.parse_args()
#outfile = args.o
#args = parser.parse_args()

#Supply your favorite JSON output of FP-Akka as input. Do python3 statstest.py --help for help
#tested against FP-Akka 1.5.2 JSON output with python3
if __name__=="__main__":
   with open(args.i) as data_file:
         fpAkkaOutput=json.load(data_file)
   normalized = True
   origin1 = [0,0]
   origin2 = [5,0]
   outfile = args.o
   workbook = xlsxwriter.Workbook(args.o)
   worksheet = workbook.add_worksheet()
   configFile= 'stats.ini'
   stats = OutcomeStats(workbook,worksheet,data_file,outfile,configFile,origin1,origin2)
   worksheet.set_column(0,len(stats.getOutcomes()), 3+stats.getMaxLength())
   print(stats.getOutcomes())
   outcomeFormats = OutcomeFormats({})
   formats = outcomeFormats.initFormats(workbook) #shouldn't be attr of main class
   validatorStats =           stats.createStats(fpAkkaOutput, ~normalized)
   validatorStatsNormalized = stats.createStats(fpAkkaOutput, normalized)
   outcomes = stats.getOutcomes()
#   print("outcomes=", outcomes)
   validators = stats.getValidators()
   stats.stats2XLSX(workbook, worksheet, formats,validatorStats,origin1, outcomes,validators)
   stats.stats2XLSX(workbook, worksheet, formats,validatorStatsNormalized,origin2, outcomes,validators)
   workbook.close()

   
