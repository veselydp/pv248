import sqlite3
import sys
import json

def parsePart(row):
    if row == "0": return False
    if row == "1": return True

def fetchVoices(score):
    voiceDict = {}
    for index, row2 in enumerate(c.execute("Select range,name from voice where score=(?)", (row[10],))):
        voiceDict[index+1] = {}
        voiceDict[index+1]["Range"]=row2[0]
        if (voiceDict[index+1]["Range"]) is None: voiceDict[index+1].pop("Range")
        voiceDict[index+1]["Name"]=row2[1]
        if (voiceDict[index+1]["Name"]) is None: voiceDict[index+1].pop("Name")
        if (len(voiceDict[index+1]) == 0): voiceDict.pop(index+1)
    return voiceDict

def fetchEditor(edition):
    personArr = []
    for index, row in enumerate(c.execute("Select person.name from edition_author join person on edition_author.editor=person.id where edition=(?)", (edition, ))):
        personArr.append(row[0])
    return personArr

def fetchComposer(scoreID):
    personArr = []
    for index, row in enumerate(c.execute("Select person.name, person.born, person.died from score_author join person on score_author.composer=person.id where score_author.score=(?)", (scoreID, ))):
        personArr.append({})
        personArr[-1]["Name"]=row[0]
        if (personArr[-1]["Name"]) is None: personArr[-1].pop("Name")
        personArr[-1]["Born"]=row[1]
        if (personArr[-1]["Born"]) is None: personArr[-1].pop("Born")
        personArr[-1]["Died"]=row[2]
        if (personArr[-1]["Died"]) is None: personArr[-1].pop("Died")
    return personArr

conn = sqlite3.connect("scorelib.dat")
conn.text_factory = str
authorDict = {}

c = conn.cursor()
authorQuery = ("%" + sys.argv[1] + "%")
rows = c.execute("Select person.name, print.id, score.name, score.genre, score.key, score.incipit, score.year, edition.year, edition.name, print.partiture, score.id, edition.id from person join score_author on person.id=score_author.composer join score on score.id=score_author.score join edition on score.id=edition.score join print on edition.id=print.edition where person.name like (?) order by person.name", (authorQuery, ))
for row in list(rows):
    if row[0] not in authorDict:
        authorDict[row[0]] = []
    checker = False
    for item in authorDict[row[0]]:
        if item["Print Number"] == row[1]:
            checker=True
    if checker == False:
        authorDict[row[0]].append({})
        currentIndex = authorDict[row[0]][-1]
        currentIndex["Print Number"] = row[1]
        currentIndex["Title"] = row[2]
        if (currentIndex["Title"]) is None: currentIndex.pop("Title")
        currentIndex["Genre"] = row[3]
        if (currentIndex["Genre"]) is None: currentIndex.pop("Genre")
        currentIndex["Key"] = row[4]
        if (currentIndex["Key"]) is None: currentIndex.pop("Key")
        currentIndex["Incipit"] = row[5]
        if (currentIndex["Incipit"]) is None: currentIndex.pop("Incipit")
        currentIndex["Composition Year"] = row[6]
        if (currentIndex["Composition Year"]) is None: currentIndex.pop("Composition Year")
        currentIndex["Publication Year"] = row[7]
        if (currentIndex["Publication Year"]) is None: currentIndex.pop("Publication Year")
        currentIndex["Edition"] = row[8]
        if (currentIndex["Edition"]) is None: currentIndex.pop("Edition")
        parBolean = (parsePart(row[9]))
        currentIndex["Partiture"] = parBolean
        if (currentIndex["Partiture"]) is None: currentIndex.pop("Partiture")
        voiceDict = fetchVoices(row[10])
        if len(voiceDict) > 0: currentIndex["Voices"] = voiceDict
        editorArr = fetchEditor(row[11])
        if len(editorArr) > 0: currentIndex["Editor"] = editorArr
        personArr = fetchComposer(row[10])
        if len(personArr) > 0: currentIndex["Composer"] = personArr

print(json.dumps(authorDict, ensure_ascii=False, indent=2 ))

#for row in c.execute("Select * from voice where score=18"):
#  print(row)
