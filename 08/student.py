import pandas as pd
from statistics import mean, median
import sys
import json
from scipy import stats, optimize
from datetime import datetime, timedelta

file = pd.read_csv(sys.argv[1])
columns = list(file.head(0))

def aggregateStuff(file):
    aggPoints = []
    numberOfStudent = (len(file[columns[0]]))
    for column in columns[1:]:
        aggPoints.append(sum(file[column])/numberOfStudent)
    aggPoints = pd.Series(aggPoints)
    aggPoints.index = columns[1:]
    print(aggPoints)
    return(aggPoints)


def daysTillBang(slope):
    sixteenPoints = 16/slope
    twentyPoints = 20/slope
    semBeg = datetime.strptime("2018-09-17", "%Y-%m-%d")
    sixteenPoints = semBeg + timedelta(days=sixteenPoints)
    sixteenPoints = sixteenPoints.strftime("%Y-%m-%d")
    twentyPoints = semBeg + timedelta(days=twentyPoints)
    twentyPoints = twentyPoints.strftime("%Y-%m-%d")
    return sixteenPoints, twentyPoints

def getDates(columns):
    semBeg = datetime.strptime("2018-09-17", "%Y-%m-%d")
    datesSinceBeg = []
    uniqueDates = []
    for date in columns[1:]:
        slash = date.find("/")
        date = date[:slash]
        date = date.strip(" ")
        dateObject = datetime.strptime(date, "%Y-%m-%d")
        dateDiff = (dateObject - semBeg)
        dateDiff = int(dateDiff.days)
        if dateDiff not in datesSinceBeg:
            uniqueDates.append(date)
            datesSinceBeg.append(dateDiff)
    return(datesSinceBeg, uniqueDates)

def getCumPoints(file, columns, uniqueDates):
    dateArr = []
    cumulTemp = 0
    for date in uniqueDates:
        for column in columns:
            if (column.find(date)) != -1:
                cumulTemp += file[column]
        dateArr.append(cumulTemp)
    return dateArr


if sys.argv[2] != "average":
    selectedStudent = file[file["student"]==int(sys.argv[2])]
    selectedStudent = selectedStudent.T
    selectedStudent = selectedStudent[0]
    selectedStudent = selectedStudent.drop("student")
else:
    selectedStudent = aggregateStuff(file)
indexes = selectedStudent.index
execDict = {}

for i, row in enumerate(selectedStudent):
    currIndex = indexes[i]
    slash = currIndex.find("/")
    currIndex = currIndex[slash+1:]
    if currIndex not in execDict:
        execDict[currIndex] = row
        #execDict[currIndex].append(row)
    else:
        execDict[currIndex] += row

execDict = pd.Series(execDict)

dateArr= {}
dateArr["mean"] = round(mean(execDict), 1)
dateArr["median"] = round(median(execDict),1)
dateArr["total"] = round(sum(execDict),2)

counter = 0
for note in execDict:
    if note > 0: counter += 1
dateArr["passed"] = counter

datesSinceBeg, uniqueDates = getDates(columns)
cumPoints = getCumPoints(selectedStudent, columns, uniqueDates)
#slope, intercept, r_value, p_value, std_err = stats.linregress(cumPoints, datesSinceBeg)
slope = optimize.curve_fit(lambda x, m: m*x, datesSinceBeg, cumPoints)[0][0]
dateArr["regression slope"] = round(slope, 1)

sixteenPoints, twentyPoints = daysTillBang(slope)
dateArr["date 16"] = sixteenPoints
dateArr["date 20"] = twentyPoints

print(json.dumps(dateArr, ensure_ascii=False, indent=2))