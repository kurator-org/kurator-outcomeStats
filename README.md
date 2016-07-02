# kurator-outcomeStats
This python app produces naive statistics from JSON produced by FP-Akka. The intent is to generalize it.

The app is based on the [xlsxWriter package](http://xlsxwriter.readthedocs.org/#)

The [journal article](http://bdj.pensoft.net/articles.php?id=992) offers a small DwCa archive with only 12 occurrences, with minor quality control issues.
##Prerequisites
* XlsWriter  See http://xlsxwriter.readthedocs.org/getting_started.html#installing-xlsxwriter.
* Python3 for now. (mainly because some function parameters are typed)
###Directories

###Files:
In kurator-outcomeStats/org/kurator/outcomestats
* OutcomeStats.py The application package<br/>
* OutcomeFormats.py Set default cell formats based on postprocessor outputs
* stats.ini  Default validators and outcomes
* statstest.py  Produces example named outcomeStats.xlsx<br/>
* occurrence_qc.json output of FP-Akka 1.5.2 (?), input to the invocation in statstest<br/>
* occurrences_922.zip The DwCa from which FP-Akka produced occurrence_qc.json ---to be supplied<br/>
* postprocessor output spreadsheet --- to be supplied<br/>

To execute test
```
python statstest.py
```



More to come soon...
