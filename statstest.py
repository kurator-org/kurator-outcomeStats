#> python3 statstest.py
#default input: occcurrence_qc.json
#default output: combined.xlsx
import json
import sys
import xlsxwriter
#import OutcomeFormats
from OutcomeStats import *
from OutcomeFormats import *
from Args import *
import argparse
#import unittest


if __name__=="__main__":
   args=Args('occurrence_qc.json', 'outcomeStats.xlsx', 'stats.ini')
   with open(args.getInfile()) as data_file:
         fpAkkaOutput=json.load(data_file)
   normalized = True
   origin1 = [0,0]
   origin2 = [5,0]
   outfile = args.getOutfile()
   workbook = xlsxwriter.Workbook(outfile)
   worksheet = workbook.add_worksheet()
   configFile= 'stats.ini'
#   stats = OutcomeStats(workbook,worksheet,data_file,outfile,configFile,origin1,origin2)
   stats = OutcomeStats(workbook,worksheet,args,origin1,origin2)
   worksheet.set_column(0,len(stats.getOutcomes()), 3+stats.getMaxLength())
#   print(stats.getOutcomes())
 #  outcomeFormats = OutcomeFormats(configFile,workbook)
   formats = OutcomeFormats(configFile,workbook)
#   formats = outcomeFormats.initFormats(workbook) #shouldn't be attr of main class
   print("fmts=", formats.getFormats())
   validatorStats =           stats.createStats(fpAkkaOutput, ~normalized)
   validatorStatsNormalized = stats.createStats(fpAkkaOutput, normalized)
   outcomes = stats.getOutcomes()
#   print("outcomes=", outcomes)
   validators = stats.getValidators()
#   stats.stats2XLSX(workbook, worksheet, formats,validatorStats,origin1, outcomes,validators)
   stats.stats2XLSX(workbook, worksheet, formats.getFormats(),validatorStats,origin1, outcomes,validators)
###   stats.stats2XLSX(workbook, worksheet, formats,validatorStatsNormalized,origin2, outcomes,validators)
   workbook.close()
