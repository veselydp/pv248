import sqlite3
import os
from scorelib import load
import sys

def checkScoreExits(record):
    for row in c.execute("Select score.name, score.id from score"):
      if (record.edition.composition.name == row[0]):
          return row[1]
    return -1

def storeVoices(compoID, record):
    # store voices
        for index, voice in enumerate(record.edition.composition.voices):
            c.execute("INSERT INTO voice(number, score, range, name) VALUES  (?, ?, ?, ?)", (index+1, compoID, voice.range, voice.name))
            conn.commit()

def storeEdition(compoID, record):
    # store edition
        c.execute("INSERT INTO edition(score, name, year) VALUES  (?, ?, ?)", (compoID, record.edition.name, None))
        conn.commit()
        editionAuthors = lookupEditionAuthor(record)
        for item in (c.execute("Select max(id) from edition")):
            editionID = item[0]
        storeEditionAuthor(editionID, editionAuthors)
        storePrint(editionID, record)

def storePrint(editionID, record):
    # store print
    c.execute("INSERT INTO print(id, partiture, edition) VALUES  (?, ?, ?)", (record.print_id, record.partiture, editionID))
    conn.commit()


def lookupCompoAuthor(data):
    compoAuthorArr = []
    for author in data.edition.composition.authors:
        for row in c.execute("Select id from person where name=?", (author.name,)):
            compoAuthorArr.append(row[0])
    return(compoAuthorArr)

def lookupEditionAuthor(data):
    authorArr = []
    for author in data.edition.authors:
        for row in c.execute("Select id from person where name=?", (author.name,)):
            authorArr.append(row[0])
    return(authorArr)

def storeEditionAuthor(editionID, authorID):
    for author in authorID:
        c.execute("INSERT INTO edition_author(edition, editor) VALUES  (?, ?)", (editionID, author))
        conn.commit()

def storeScoreAuthor(compoID, authorID):
    for author in authorID:
        c.execute("INSERT INTO score_author(score, composer) VALUES  (?, ?)", (compoID, author))
        conn.commit()


os.system("sqlite3 " + sys.argv[2] + " < scorelib.sql")
data = load(sys.argv[1])

conn = sqlite3.connect(sys.argv[2])
conn.text_factory = str

c = conn.cursor()

# store composition authors
for record in data:
    for author in (record.edition.composition.authors):
        if (author.name != ""):
            checker = False
            for row in c.execute("Select name from person"):
                if author.name == row[0]: checker = True
            if checker == False: c.execute("INSERT INTO person(name, born, died) VALUES  (?, ?, ?)", (author.name, author.born, author.died))
            if checker == True:
                for row in c.execute("Select * from person"):
                    if author.name == row[3]:
                        if author.born is not None and row[1] is None:
                            c.execute("UPDATE person SET born=(?) where id=(?)", (author.born, row[0], ))
                        if author.died is not None and row[2] is None:
                            c.execute("UPDATE person SET died=(?) where id=(?)", (author.died, row[0], ))
            conn.commit()

    # store edition authors
    for author in (record.edition.authors):
        checker = False
        for row in c.execute("Select name from person"):
            if author.name == row[0]: checker = True
        if checker == False:
            c.execute("INSERT INTO person(name, born, died) VALUES  (?, ?, ?)", (author.name, None, None))
        if checker == True:
            for row in c.execute("Select * from person"):
                if author.name == row[3]:
                    if author.born is not None and row[1] is None:
                        c.execute("UPDATE person SET born=(?) where id=(?)", (author.born, row[0], ))
                    if author.died is not None and row[2] is None:
                        c.execute("UPDATE person SET died=(?) where id=(?)", (author.died, row[0], ))
        conn.commit()



# store composition
for record in data:
    returnedScore = checkScoreExits(record)
    if returnedScore == -1:
        c.execute("INSERT INTO score(name, genre, key, incipit, year) VALUES  (?, ?, ?, ?, ?)", (record.edition.composition.name, record.edition.composition.genre, record.edition.composition.key, record.edition.composition.incipit, record.edition.composition.year))
        conn.commit()
        for item in (c.execute("Select max(id) from score")):
            compoID = int(item[0])
    else: compoID = returnedScore
    compoAuthors = lookupCompoAuthor(record)
    storeScoreAuthor(compoID,compoAuthors)
    storeVoices(compoID, record)
    storeEdition(compoID, record)


 #for row in c.execute("Select person.name from person"):
 # print(row)

#for row in c.execute("Select person.name from edition join edition_author on edition.id=edition_author.edition join person on edition_author.editor=person.id"):
#    print(row)
