# kurator-outcomeStats
This python app produces naive statistics from JSON produced by FP-Akka. The intent is to generalize it.

The app is based on the [xlsxWriter package](http://xlsxwriter.readthedocs.org/#)

The [journal article](http://bdj.pensoft.net/articles.php?id=992) offers a small DwCa archive with only 12 occurrences, with minor quality control issues.
###Directories

###Files:
In kurator-outcomeStats/org/kurator/outcomestats
** outcomestats.py The application package<br/>
** statstest.py  Produces example named combined.xlsx
** occurrence_qc.json output of FP-Akka 1.5.2 (?), input to the invocation in statstest<br/>
* occurrences_922.zip The DwCa from which FP-Akka produced occurrence_qc.json ---to be supplied<br/>
* postprocessor output spreadsheet --- to be supplied<br/>

To execute, start python3, and execute
```
exec(open("outcomeStats.py").read())
```
The result executes the unit test beginning at line 120


More to come soon...
