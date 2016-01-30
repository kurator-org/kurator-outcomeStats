import json
import sys
import xlsxwriter

class OutcomeFormats:
   def __init__(self, outcomes):
      
      def getOutcomes(self):
         return outcomes
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

   
