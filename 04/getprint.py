import sqlite3
import sys
import json


conn = sqlite3.connect("scorelib.dat")
conn.text_factory = str

c = conn.cursor()

authorList = []

for row in c.execute("Select person.name, person.born, person.died from print join edition on print.edition=edition.id join score_author on score_author.score=edition.score join person on score_author.composer=person.id where print.id=(?)", (int(sys.argv[1]), )):
    dict = {
        "name" : row[0],
        "born" : row[1],
        "died" : row[2]
    }
    authorList.append(dict)

for author in authorList:
    if (author["born"]) is None: author.pop("born")
    if (author["died"]) is None: author.pop("died")
    if (author["name"]) is None: author.pop("name")

print(json.dumps(authorList, ensure_ascii=False, indent=1 ))
