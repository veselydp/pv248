import pandas as pd
from statistics import mean, median
import sys
import json


file = pd.read_csv(sys.argv[1])
columns = list(file.head(0))

def countStat(dateArr):
    varDict = {}
    for exercise in dateArr:
        if exercise not in varDict: varDict[exercise] = {}
        varDict[exercise]["mean"] = round(mean(dateArr[exercise]), 2)
        varDict[exercise]["median"] = median(dateArr[exercise])
        varDict[exercise]["first"] = dateArr[exercise].quantile(.25)
        varDict[exercise]["last"] = dateArr[exercise].quantile(.75)

        counter = 0
        for row in (dateArr[exercise]):
            if row  >= 1: counter += 1
        varDict[exercise]["passed"] = counter
    return varDict

def dates(columns):
    dateArr = {}
    for i in range(1,len(columns)):
        curFile = file[columns[i]]
        counter = 0
        for row in (file[columns[i]]):
            if row >= 1: counter += 1
        colName = columns[i].strip(" ")
        slahPos = colName.find("/")
        colName = colName[:slahPos]
        if colName not in dateArr:
            dateArr[colName] = curFile
        else:
            dateArr[colName] = pd.concat([curFile, dateArr[colName]])
    varDict = countStat(dateArr)
    print(json.dumps(varDict, ensure_ascii=False, indent=2))




def deadlines(columns):
    dateArr = {}
    for i in range(1,len(columns)):
        counter = 0
        for row in (file[columns[i]]):
            if row >= 1: counter += 1
        colName = "%02d" % (i,)
        dateArr[colName] = {}
        dateArr[colName]["passed"] = counter
        dateArr[colName]["mean"] = round(mean(file[columns[i]]), 2)
        dateArr[colName]["median"] = median(file[columns[i]])
        dateArr[colName]["first"] = file[columns[i]].quantile(.25)
        dateArr[colName]["last"] = file[columns[i]].quantile(0.75)
    print(json.dumps(dateArr, ensure_ascii=False, indent=2))


def exercises(columns):
    dateArr = {}
    for i in range(1, len(columns)):
        curFile = file[columns[i]]
        slashIndex = (columns[i].find("/"))
        curExec = (columns[i][slashIndex+1:])
        curFile.name = (curExec)
        if curExec not in dateArr:
            dateArr[curExec] = curFile
        else:
            dateArr[curExec] = pd.concat([curFile, dateArr[curExec]])
    varDict = countStat(dateArr)
    print(json.dumps(varDict, ensure_ascii=False, indent=2))






if sys.argv[2] == "dates": dates(columns)
if sys.argv[2] == "deadlines": deadlines(columns)
if sys.argv[2] == "exercises": exercises(columns)
