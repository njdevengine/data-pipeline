
print(r"""
 __             _              _                    
/ _\_ __   __ _| | _____      | |__   __ _ ___  ___ 
\ \| '_ \ / _` | |/ / _ \_____| '_ \ / _` / __|/ _ \
_\ \ | | | (_| |   <  __/_____| |_) | (_| \__ \  __/
\__/_| |_|\__,_|_|\_\___|     |_.__/ \__,_|___/\___|

                           ____
  ________________________/ 0 0\______/
 <_O_O_O_O_O_O_O_O_O_O_O_O_____/      \

""")
#IMPORT DEPENDENCIES
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import random
import warnings
import numpy as np
import datetime
from datetime import date
currentDT = datetime.datetime.now()

warnings.simplefilter(action='ignore', category=FutureWarning)
then = time.time() #Time before the operations start


print("Dependencies Imported...")

## Getting File
input_path = r'file.xlsx'
output_path = r"file"+str(date.today())+".csv"

file = pd.read_excel(input_path,encoding = "UTF-8")
file.to_csv("snake_file_input.csv")
print("Retrieved File...")

## Getting Business Partners
import requests
with requests.Session() as s:
    url = "login url goes here"
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    r = s.get(url, headers=headers)
login_data = {"loginid": "yourlogin",
"password": "yourpass",
"SignIn":""}
r = s.post(url, data =login_data, headers=headers)
url = "target csv url"
r = s.get(url)
print("Got database Business Partners...")

import csv
with open("Businesspartnerpy.csv", "w", encoding="UTF-8") as f:
    writer = csv.writer(f)
    reader = csv.reader(r.text.splitlines())
    for row in reader:
        writer.writerow(row)

import pandas as pd
path = "Businesspartnerpy.csv"
df = pd.read_csv(path,encoding = "utf-8")
df.to_csv("Business_CSV.csv",encoding = "utf-8", index =False, header = True)

db = df[["Record ID#","Full Business Name","Contact Person Name 1","Contact Person Name 2","Phone 1",
         "Phone 2","Phone 3","Business Email 1","Business Email 2","Business Email 3"]]

#SHOW HEADERS FOR BOTH FILES
dheaders = list(db)
fheaders = list(file)
print("Lookup file: ")
print("-------------------")
[print(i) for i in fheaders]
print("\n")
print("database: ")
print("-------------------")
[print(i) for i in dheaders][0]

#GENERATE db NAME DICTIONARY dbname_dict
db_dict = pd.Series(db['Full Business Name'].values,index=df["Record ID#"]).to_dict()
dbname_dict = {}
for i in db_dict:
    dbname_dict[i] = []
    try:
        dbname_dict[i].append(db_dict[i].split(" DBA ")[0])
        dbname_dict[i].append(db_dict[i].split(" DBA ")[1])
        dbname_dict[i].append(db_dict[i].split(" DBA ")[2])
        dbname_dict[i].append(db_dict[i].split(" DBA ")[3])
    except:
        pass

file_dict = pd.Series(file['Business Name'].values,index=file.index).to_dict()
file_dict2 = pd.Series(file['Business DBA'].values,index=file.index).to_dict()

#CREATE THE LOOKUP NAME DICTIONARIES
fname_dict = {}
x = 0
for i in file_dict2:
    fname_dict[i] = []
    try:
        fname_dict[i].append(file_dict2[i].split(" DBA ")[0])
        fname_dict[i].append(file_dict2[i].split(" DBA ")[1])
        fname_dict[i].append(file_dict2[i].split(" DBA ")[2])
    except:
        x+=1

#MERGE THE NAME AND DBA FIELD DICTIONARIES: FILE 
for i in fname_dict:
    fname_dict[i].append(file_dict[i])

#CREATE dataBASE EMAIL DICTIONARY
dbe_dict = pd.Series(db['Business Email 1'].values,index=df["Record ID#"]).dropna().to_dict()
dbe_dict2 = pd.Series(db['Business Email 2'].values,index=df["Record ID#"]).dropna().to_dict()
dbe_dict3 = pd.Series(db['Business Email 3'].values,index=df["Record ID#"]).dropna().to_dict()
dbemail_dict = {}
for i in dbe_dict:
    dbemail_dict[i] = []
    dbemail_dict[i].append(dbe_dict[i])
    try:
        dbemail_dict[i].append(dbe_dict2[i])
        dbemail_dict[i].append(dbe_dict3[i])
    except:
        pass

#CREATE dataBASE NUMBER DICTIONARY
dbn_dict = pd.Series(db['Phone 1'].values,index=df["Record ID#"]).dropna().to_dict()
dbn_dict2 = pd.Series(db['Phone 2'].values,index=df["Record ID#"]).dropna().to_dict()
dbn_dict3 = pd.Series(db['Phone 3'].values,index=df["Record ID#"]).dropna().to_dict()
dbnum_dict = {}
for i in dbn_dict:
    dbnum_dict[i] = []
    dbnum_dict[i].append(dbn_dict[i])
    try:
        dbnum_dict[i].append(dbn_dict2[i])
        dbnum_dict[i].append(dbn_dict3[i])
    except:
        pass

#CREATE FILE NUMBER DICTIONARY
fn_dict = pd.Series(file['Phone 1'].values,index=file.index).dropna().to_dict()
fn_dict2 = pd.Series(file['Phone 2'].values,index=file.index).dropna().to_dict()
try:
    fn_dict3 = pd.Series(file['Phone 3'].values,index=file.index).dropna().to_dict()
except:
    pass
fnum_dict = {}
for i in fn_dict:
    fnum_dict[i] = []
    fnum_dict[i].append(fn_dict[i])
    try:
        fnum_dict[i].append(fn_dict2[i])
        fnum_dict[i].append(fn_dict3[i])
    except:
        pass

#CREATE FILE EMAIL DICTIONARY
fe_dict = pd.Series(file['Business Email 1'].values,index=file.index).dropna().to_dict()
fe_dict2 = pd.Series(file['Business Email 2'].values,index=file.index).dropna().to_dict()
try:
    fe_dict3 = pd.Series(file['Business Email 3'].values,index=file.index).dropna().to_dict()
except:
    pass
femail_dict = {}
for i in fe_dict:
    femail_dict[i] = []
    femail_dict[i].append(fe_dict[i])
    try:
        femail_dict[i].append(fe_dict2[i])
        femail_dict[i].append(fe_dict3[i])
    except:
        pass

#CREATE FILE CONTACT DICTIONARY
fc_dict = pd.Series(file['Contact Person Name 1'].values,index=file.index).dropna().to_dict()
fc_dict2 = pd.Series(file['Contact Person Name 2'].values,index=file.index).dropna().to_dict()
fcontact_dict = {}
for i in fc_dict:
    fcontact_dict[i] = []
    fcontact_dict[i].append(fc_dict[i])
    try:
        fcontact_dict[i].append(fc_dict2[i])
    except:
        pass

#CREATE dataBASE CONTACT DICTIONARY
dbc_dict = pd.Series(db['Contact Person Name 1'].values,index=df["Record ID#"]).dropna().to_dict()
dbc_dict2 = pd.Series(db['Contact Person Name 2'].values,index=df["Record ID#"]).dropna().to_dict()
dbcontact_dict = {}
for i in dbc_dict:
    dbcontact_dict[i] = []
    dbcontact_dict[i].append(dbc_dict[i])
    try:
        dbcontact_dict[i].append(dbc_dict2[i])
    except:
        pass
print("Dictionaries Created...")

#NAME MATCHING SCRIPT
fid = []
file_match = []
db_match = []
match_score = []
match = []
dbid = []
for a in fname_dict:
    for b in fname_dict[a]:
        for c in dbname_dict:
            for d in dbname_dict[c]:
                if fuzz.token_sort_ratio(b,d) >=90:
                    m = fuzz.token_sort_ratio(b,d)
                    fid.append(a)
                    file_match.append(b)
                    dbid.append(c)
                    db_match.append(d)
                    match_score.append(m)
                    result ="%s %s / %s %s / Match: %s" % (a,b,c,d,m)
                    match.append(result)
print("Names Matched...")

#Email Matching Script
for a in femail_dict:
    for b in femail_dict[a]:
        for c in dbemail_dict:
            for d in dbemail_dict[c]:
                if fuzz.token_sort_ratio(b,d) >=70:
                    m = fuzz.token_sort_ratio(b,d)
                    fid.append(a)
                    file_match.append(b)
                    dbid.append(c)
                    db_match.append(d)
                    match_score.append(m)
                    result ="%s %s / %s %s / Match: %s" % (a,b,c,d,m)
                    match.append(result)
print("Emails Matched...")

#NUMBER MATCHING SCRIPT
for a in fnum_dict:
    for b in fnum_dict[a]:
        for c in dbnum_dict:
            for d in dbnum_dict[c]:
                if b==d:
                    m = 100
                    fid.append(a)
                    file_match.append(b)
                    dbid.append(c)
                    db_match.append(d)
                    match_score.append(m)
                    result ="%s %s / %s %s / Match: %s" % (a,b,c,d,m)
                    match.append(result)
print("Numbers Matched...")

#CONTACT MATCHING SCRIPT
for a in fcontact_dict:
    for b in fcontact_dict[a]:
        for c in dbcontact_dict:
            for d in dbcontact_dict[c]:
                if fuzz.token_sort_ratio(b,d) >=90:
                    m = fuzz.token_sort_ratio(b,d)
                    fid.append(a)
                    file_match.append(b)
                    dbid.append(c)
                    db_match.append(d)
                    match_score.append(m)
                    result ="%s %s / %s %s / Match: %s" % (a,b,c,d,m)
                    match.append(result)
print("Contacts Matched...")

fuzzy_dataframe = pd.DataFrame({'Record ID#':dbid,'file_match': file_match, 'database_match': db_match,
                                'match_score': match_score,'match':match})
fuzzy_dataframe.to_csv(r'matches.csv')
fuzzy_dataframe.to_csv('snake_matches_'+str(date.today())+'.csv')
print("Check Root for snake_matches.csv...")

data_input = []
for i in range(len(match)):
    data ="RID#: %s / %s / %s" % (dbid[i],db_match[i],match_score[i])
    data_input.append(data)

import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

x = file
file = pd.read_excel(input_path,encoding = "UTF-8")
headers = list(x.columns.values)
for h in headers:
    for i in range(len(db_match)):
        x.loc[x[h] == file_match[i], h] = data_input[i]
        x.loc[x['Business DBA'].str.contains(file_match[i], na=False), 'Business DBA'] = data_input[i]

x = x.reset_index()
file = file.reset_index()
x["file"] = "B"
file["file"] = "A"
frames = [x, file]
result = pd.concat(frames)
result["File_Index"] = result["index"].map(str) + result["file"]
result = result.sort_values(by=['File_Index'])
result = result.drop(columns =['file','index'])
result["result_date"] = currentDT.strftime("%m/%d/%Y")
result.to_csv(output_path, index=False)

print("Matching Complete.")

now = time.time() #Time after it finished
seconds = round(now-then,2)
print("It took: ", seconds, " seconds")
leads = len(file)
leads_per_second = round(leads/seconds,2)
print(leads_per_second,"Leads Per Second")
print (str(currentDT))
