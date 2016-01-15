#exec(open("statstest.py").read()) to load
import json
import sys
import xlsxwriter
#from outcomestats import stats2XLSX
#from outcomestats import createStats
from outcomestats import *

import unittest
#from ..outcomestats import outcomestats
#unit test. Supply your favorite outcome of FP-Akka
#tested against FP-Akka 1.5.2 JSON output with python3
with open('occurrence_qc.json') as data_file:
   fpAkkaOutput=json.load(data_file)
normalized = True
validatorStats =           createStats(fpAkkaOutput, ~normalized)
validatorStatsNormalized = createStats(fpAkkaOutput, normalized)
origin1 = [0,0]
origin2 = [5,0]
outfile="combined.xlsx"
workbook = xlsxwriter.Workbook(outfile)
formats=initFormats(workbook)
worksheet = workbook.add_worksheet()
worksheet.set_column(0,len(outcomes), 3+maxlength)
stats2XLSX(workbook, worksheet, formats,validatorStats,origin1, outcomes,validators)
stats2XLSX(workbook, worksheet, formats,validatorStatsNormalized,origin2, outcomes,validators)
workbook.close()
