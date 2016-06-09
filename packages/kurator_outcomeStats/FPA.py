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
__version__ = "FPA.py 2016-05-28T17:38:34-0400"

import json
import xlsxwriter
import argparse
import logging
from dwca_utils import response
from dwca_utils import setup_actor_logging

def FPA1(options):
   """Build options to prepare for instance of class FPA
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
        
   print("In FPA1")
   
def _getoptions():
    """Parse command line options and return them."""
    parser = argparse.ArgumentParser()

    help = 'Name  of the file from which to read QC records (required)'
    parser.add_argument("-r", "--inputfile", help=help)

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
   
def main():
  # print 'starting main'
   options = _getoptions()
   optdict = {}

   if options.inputfile is None or len(options.inputfile)==0:
      s = 'Xsyntax:\n'
      s += 'python FPA1.py'
      s += ' -w ./workspace'
      s += ' -l DEBUG'
      print '%s' % s
#      return

   optdict['inputfile'] = options.inputfile
   optdict['workspace'] = options.workspace
   optdict['worksheetname'] = options.worksheetname
   optdict['outputfile'] = options.outputfile
   optdict['loglevel'] = options.loglevel
   optdict['outcomes'] = options.outcomes
   print 'optdict: %s' % optdict

   response = FPA1(optdict)
   print '\nresponse: %s' % response
   return

if __name__ == '__main__':
    main()    
