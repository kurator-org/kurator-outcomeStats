#> python3 statstest.py
#default input: occcurrence_qc.json
#default output: combined.xlsx
import json
import sys
import xlsxwriter
from outcomestats import *
import argparse
#import unittest

parser = argparse.ArgumentParser()
parser.add_argument('--i',default='occurrence_qc.json', help="Defaults to occurrence_qc.json if '--i' absent")
parser.add_argument('--o',default='outcomeStats.xlsx', help="Defaults to outcomeStats.xlsx if '--o' absent")
args = parser.parse_args()
#outfile = args.o
#args = parser.parse_args()

#Supply your favorite JSON output of FP-Akka as input. Do python3 statstest.py --help for help
#tested against FP-Akka 1.5.2 JSON output with python3
if __name__=="__main__":
   with open(args.i) as data_file:
         fpAkkaOutput=json.load(data_file)
   normalized = True
   validatorStats =           createStats(fpAkkaOutput, ~normalized)
   validatorStatsNormalized = createStats(fpAkkaOutput, normalized)
   origin1 = [0,0]
   origin2 = [5,0]
   outfile = args.o
   workbook = xlsxwriter.Workbook(args.o)
   formats=initFormats(workbook)
   worksheet = workbook.add_worksheet()
   worksheet.set_column(0,len(outcomes), 3+maxlength)
   stats2XLSX(workbook, worksheet, formats,validatorStats,origin1, outcomes,validators)
   stats2XLSX(workbook, worksheet, formats,validatorStatsNormalized,origin2, outcomes,validators)
   workbook.close()
