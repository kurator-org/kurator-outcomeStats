import xlsxwriter
import configparser
#from collections import OrderedDict

class OutcomeFormats:
   """Class supporting xlsx cell formats for a set of Kurator Quality Control *outcomes*
   """
   def __init__(self, configFile, workbook):
       parser = configparser.ConfigParser()   #python 2.7 and 3 default Dict to OrderedDict 
       parser.sections()
       self.configFile = configFile
       parser.read(configFile)
       self.outcome_colors = eval(parser['DEFAULT']['outcome_colors'])  #assumes outcome_colors in the order of columns desired
       self.formats= {}
       for outcome, color in self.outcome_colors.items():
           self.formats[outcome] = workbook.add_format()
           self.formats[outcome].set_bg_color(color)
       self.typography=workbook.add_format({'bold': True})
       
   def initFormats(self, workbook):
      self.workbook = workbook
      #get the outcome colors dict from the configFile

      
   def getTypography(self):
      return self.typography 

   def getValidators(self):
      return self.outcome_colors.keys()

   def getFormat(self, outcome):
      return self.formats[outcome]
   def getFormats(self):
       return self.formats
   
   def getWorkbook(self):
       return self.workbook

   def getOutcomes(self):
       return self.outcome_colors.keys()  #order preserved???
       
   def getOutcomeColors(self):  
       return self.outcome_colors.values() #order preserved?? 

   def getFormat(self, outcome):
       return self.format #formats

   def getFormats(self):  #
       return self.formats
       

   def loadWorkbook(self,workbook):
      for outcome,format in self.formats.items():
         idx = self.outcomes.index(outcome)
         color = self.outcomeColors(idx)
         format.set_bg_color(color)
         workbook.add_format()

def main():
   print("OutcomeFormats.main()")
   import statstest
   exec(open("statstest.py").read())
if __name__ == "__main__" :
   main()
