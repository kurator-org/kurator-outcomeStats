import json
import xlsxwriter
import configparser
#exec(open("outcomeStats.py").read()) to load

config = configparser.ConfigParser()
config.sections()
config.read('stats.ini')

#validators=("ScientificNameValidator","DateValidator",  "GeoRefValidator",
#            "BasisOfRecordValidator") #row order in output
validators =eval( config['DEFAULT']['validators'])
maxlength= max(len(s) for s in validators)


# outcomes= ("CORRECT","CURATED","FILLED_IN", "UNABLE_DETERMINE_VALIDITY",  "UNABLE_CURATE") #col order in output
outcomes = eval(config['DEFAULT']['outcomes'])
#print(outcomes)
max1= max(len(s) for s in validators)
max2= max(len(t) for t in outcomes)
maxlength = max(max1,max2)
#print(maxlength)
#TODO: load above from a config file but default to these

###initializations

def initStats(outcomes) :
   stats = {}
   for outcome in outcomes:
       stats[outcome] = 0
   return stats

def initValidatorStats(validators, outcomes) :
   stats = {}
   for v in validators :
      stats[v] = initStats(outcomes)
   return stats

def updateValidatorStats(fpa, stats, record)  :
   data=fpa[record]["Markers"]
#   print("in updateValidatorStats[",record,"]")
   for data_k, data_v in data.items() :
      for stats_k, stats_v in stats.items() :
         if (stats_k == data_k):
            stats[stats_k][data_v] += 1
   return stats


def createStats(fpa, normalize:bool):
   validatorStats = initValidatorStats(validators, outcomes)
   for record in range(len(fpa)):
      updateValidatorStats(fpa, validatorStats, record) 
   if normalize == True :
      normalizeStats(fpa,validatorStats)
   return validatorStats

def normalizeStats(fpa,stats):
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

def stats2CSV(stats, outfile, outcomes, validators):
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

def initFormats(workbook):
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
   formats={'UNABLE_DETERMINE_VALIDITY':formatGryFill, 'CURATED':formatYelFill, 'UNABLE_CURATE':formatRedFill, 'CORRECT':formatGrnFill, 'FILLED_IN':formatMusFill}
   return formats

def stats2XLSX(workbook, worksheet, formats, stats, origin, outcomes, validators):
#   print("fmts=",formats)
   bold = workbook.add_format({'bold': True})
#   print("stats=",stats)
#   print("outcomes=", outcomes)
#   print(origin)
   worksheet.write(origin[0],origin[1],"Validator",bold)
   for str in outcomes :
      col=1+origin[1]+outcomes.index(str) #insure order is as in outcomes list
      worksheet.write(origin[0],col, str, bold) #write col header
   for k, v in stats.items():
#      print("key=",k,"val=", v)
      row = 1+origin[0]+validators.index(k) #put rows in order of the validators list
#      print("row=",row)
      worksheet.write(row,0,k) #write validator name
      #write data for each validator in its own row
      for outcome, statval in v.items():
         col=1+outcomes.index(outcome) #put cols in order of the outcomes list
         worksheet.write(row, col, statval,formats.get(outcome))
