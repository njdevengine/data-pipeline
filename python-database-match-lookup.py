#script automates database lookup for business names, emails, contacts, and phone numbers
#data entry team identifies contact information input into a template file and a script is run on a schedule
#results are output to a file, fuzzy matching is used for some fields to account for variation in spelling etc.
#dictionaries are created for all fields in order to preserve record id's
#variable naming:
#file is the file dataframe, db is the database dataframe
#NAMES
#dbname_dict, fname_dict
#EMAILS
#dbemail_dict, femail_dict
#PHONES
#dbnum_dict, fnum_dict
#CONTACT
#dbcontact_dict, fcontact_dict

#IMPORT DEPENDENCIES
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

## Getting File
file = pd.read_excel(r'F:\Username\formatted_file.xlsx',encoding = "UTF-8")

## Getting DB Data
import requests
with requests.Session() as s:
    url = "https://signin.com/sign-in-form"
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    r = s.get(url, headers=headers)
login_data = {"loginid": "you@youremail.com",
"password": "your pass",
"SignIn":""}
r = s.post(url, data =login_data, headers=headers)
url = "https://spreadsheetlink.com/file.csv"
r = s.get(url)

import csv
with open("database.csv", "w", encoding="UTF-8") as f:
    writer = csv.writer(f)
    reader = csv.reader(r.text.splitlines())
    for row in reader:
        writer.writerow(row)

import pandas as pd
path = "database.csv"
df = pd.read_csv(path,encoding = "utf-8")
df.to_csv("test_db_output.csv",encoding = "utf-8", index =False, header = True)

db = df[["Record ID#","Full Person Name","Contact Person Name 1","Contact Person Name 2","Phone 1",
         "Phone 2","Phone 3","Person Email 1","Person Email 2","Person Email 3"]]

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
db_dict = pd.Series(db['Full Person Name'].values,index=df["Record ID#"]).to_dict()
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

file_dict = pd.Series(file['Full Person Name'].values,index=file.index).to_dict()
file_dict2 = pd.Series(file['Person DBA'].values,index=file.index).to_dict()

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

#CREATE database EMAIL DICTIONARY
dbe_dict = pd.Series(db['Person Email 1'].values,index=df["Record ID#"]).dropna().to_dict()
dbe_dict2 = pd.Series(db['Person Email 2'].values,index=df["Record ID#"]).dropna().to_dict()
dbe_dict3 = pd.Series(db['Person Email 3'].values,index=df["Record ID#"]).dropna().to_dict()
dbemail_dict = {}
for i in dbe_dict:
    dbemail_dict[i] = []
    dbemail_dict[i].append(dbe_dict[i])
    try:
        dbemail_dict[i].append(dbe_dict2[i])
        dbemail_dict[i].append(dbe_dict3[i])
    except:
        pass

#CREATE database NUMBER DICTIONARY
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
fe_dict = pd.Series(file['Person Email 1'].values,index=file.index).dropna().to_dict()
fe_dict2 = pd.Series(file['Person Email 2'].values,index=file.index).dropna().to_dict()
try:
    fe_dict3 = pd.Series(file['Person Email 3'].values,index=file.index).dropna().to_dict()
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

#CREATE database CONTACT DICTIONARY
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

#Email Matching Script
for a in femail_dict:
    for b in femail_dict[a]:
        for c in dbemail_dict:
            for d in dbemail_dict[c]:
                if fuzz.token_sort_ratio(b,d) >=95:
                    m = fuzz.token_sort_ratio(b,d)
                    fid.append(a)
                    file_match.append(b)
                    dbid.append(c)
                    db_match.append(d)
                    match_score.append(m)
                    result ="%s %s / %s %s / Match: %s" % (a,b,c,d,m)
                    match.append(result)

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

fuzzy_dataframe = pd.DataFrame({'Record ID#':dbid,'file_match': file_match, 'database_match': db_match,
                                'match_score': match_score,'match':match})
fuzzy_dataframe.to_csv('fuzzy_matches.csv')
