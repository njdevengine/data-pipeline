# data-pipeline
## using fuzzywuzzy to prevent duplicate db records
* grabs data from a database and a shared folder and compares fields against one another to avoid creating duplicate records.
* gets same domain email matches, but doesn't return common emails like gmail. ie. you@gmail.com and me@gmail.com are not a match... but you@companyname.com and me@companyname.com are a match.
* requires pandas, and fuzzywuzzy
![Snake-Base](snake.jpg)
Can be Run with Windows Task Scheduler,
to find your python.exe run this code separately:
(this is the program that is run, the arguments is the path to the script.)
```
import sys
print("Python EXE : " + sys.executable)
```
