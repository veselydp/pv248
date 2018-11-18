import sys
import re

personDict = {}
centuryDict = {}

def parsePerson(line):
    personList = (line.split(";"))
    personObject = []
    # remove spaces
    for index, person in enumerate(personList):
        person = person.strip()
        #if person.find("Teleman") != -1: print(person)
        if (re.search(r'\d', person)) is not None:
            person = person.split("(")[0]
            person = person.strip()
        checker = False
        for item in personObject:
            if (item==person): checker = True
        if checker==False:
            personObject.append(person)
    return personObject

def addPersonToArr(person):
    if person in personDict:
        personDict[person] += 1
    if person not in personDict:
        personDict[person] = 1

def parseCentury(century):
    centuryParsed = None
    century = century.strip()
    try:
        centuryParsed = re.search(r"[0-9]{4}", century)
        centuryParsed = (int(centuryParsed.group()))
    except:
        pass
    if century.find("th") != -1:
        centuryFinder = century.find("th")
        centuryParsed = century[centuryFinder-2:centuryFinder] + "00"
        centuryParsed = int(centuryParsed)

    if centuryParsed is not None:
        centuryParsed = (1 + (centuryParsed - 1) // 100)
        if centuryParsed in centuryDict:
            centuryDict[centuryParsed] += 1
        if centuryParsed not in centuryDict:
            centuryDict[centuryParsed] = 1

for line in open(sys.argv[1], 'r'):
    splitLine = (line.split(":"))
    try:
        splitLine[1] = (splitLine[1].strip())
    except:
        pass
    #if splitLine[0] == "Print Number": print(splitLine[1])
    if splitLine[0] == "Composer":
        for person in parsePerson(splitLine[1]):
            addPersonToArr(person)
    if splitLine[0] == "Composition Year":
            parseCentury(splitLine[1])

if sys.argv[2] == "composer":
    for item in personDict:
        if item != "":
            print (item + ": " + str(personDict[item]))

if sys.argv[2] == "century":
    for item in centuryDict:
        if item == 21:
            helperStr = "st"
        else:
            helperStr = "th"
        print (str(item) + helperStr + " century: " + str(centuryDict[item]))
