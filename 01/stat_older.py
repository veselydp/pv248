import sys
import re

def returnAbr(name):
    part = ""
    for item in (name.split(" ")):
        if (item[0:1] != "(") and (item[0:1] != " ") and (item[0:1] != ""):
            part += (item[0:1] + ".")
    return part


def storeToDict(regExp, lineContent, lineEnd):
        #print (lineContent[regExp.start():regExp.end()-1])
        #print (lineContent[regExp.end()+1:lineEnd.start()])
        if (lineContent[regExp.start():regExp.end()-1]) != "Print Number" and lineEnd is not None:
            if (lineContent[regExp.start():regExp.end() - 1]) == "Composer":
                for name in (lineContent[regExp.end() + 1:lineEnd.start()]).split("; "):
                    nameHelper = (name[name.find(", "):])
                    if (nameHelper[3:4]) != ".":
                        if (nameHelper[3:4]) == "" and (nameHelper[2:3]) != "":
                            name = (name[:name.find(", ")] + nameHelper + ".")
                        else:
                            part = returnAbr(nameHelper[2:])
                            name = (name[:name.find(", ")] + " " + part)
                            # check for brackets
                            if name.find("(") != -1: name = name[:name.find("(")]
                            # check for empty name
                dict[lineContent[regExp.start():regExp.end() - 1]] = name

            else:
                dict[lineContent[regExp.start():regExp.end()-1]] = lineContent[regExp.end()+1:lineEnd.start()]
        if (lineContent[regExp.start():regExp.end() - 1]) == "Incipit":
            return dict

def storeComposer(line):
    if line["Composer"] in composerList:
        composerList[line["Composer"]] += 1
    else:
        composerList[line["Composer"]] = 1


def storeCentury(line):
    rCentury = re.compile(r"[0-9]{4}")
    rCenturyCompiled = rCentury.search(line["Composition Year"])
    if rCenturyCompiled is not None:
        if int(int(rCenturyCompiled.group())/100+1) in centuryList:
            centuryList[int(int(rCenturyCompiled.group())/100+1)] += 1
        else:
            centuryList[int(int(rCenturyCompiled.group())/100+1)] = 1


rDot = re.compile(r"(.*):")
rLine = re.compile(r"\n")
dict = {}
dictArray = []
composerList = {}
centuryList = {}

for line in open(sys.argv[1], 'r'):
    regResp = rDot.search(line)
    regRespLine = rLine.search(line)
    if regResp is None:
        continue
    else:

                oneRecord = storeToDict(regResp, line, regRespLine)
                # skip none records
                if oneRecord is not None:
                    # skip those records with empty composer
                    if len(oneRecord["Composer"]) > 1:
                        storeComposer(oneRecord)
                        storeCentury(oneRecord)
                        dictArray.append(oneRecord)

if sys.argv[2] == "composer":
    for composer in composerList.keys():

        print (composer + ": " + str(composerList[composer]))
        # storeToDict(line,regResp.group())
if sys.argv[2] == "century":
    for century in centuryList.keys():
        print (str(century) + "th century" + ": " + str(centuryList[century]))
