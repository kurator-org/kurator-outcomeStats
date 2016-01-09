# kurator-outcomeStats
This python app produces naive statistics from JSON produced by FP-Akka. The intent is to generalize it.

The app is based on the [xlsxWriter package](http://xlsxwriter.readthedocs.org/#)

The [journal article](http://bdj.pensoft.net/articles.php?id=992) offers a small DwCa archive with only 12 occurrences, with minor quality control issues.

###Files:
* outcomeStats.py The application <br/>
* combined.xlsx  output of the application <br/>
* occurrences_922.zip The DwCa <br/>
* occurrence_qc.json output of FP-Akka 1.5.2 (?), input to the application <br/>
* postprocessor output spreadsheet --- to be supplied<br/>

To execute, start python3, and execute
```
exec(open("outcomeStats.py").read())
```
The result executes the unit test beginning at line 115

NOTE: The file combined.xslx in this repository was hand-edited to make the column widths optimal. The actual output should have no other differences from what the app produces. This was done because the xlsxwriter package inherantly cannot process this other that by a hack described in Issue #1




More to come soon...
