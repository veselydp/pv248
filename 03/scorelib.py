import re

def load(filename):
    printArray = []
    voiceArray = []
    personArray = []
    for line in open(filename, 'r'):
        splitLine = (line.split(":"))
        try:
            splitLine[1] = (splitLine[1].strip())
        except:
            pass
        if splitLine[0] == "Incipit":
            lineBreak = True
        else:
            lineBreak = False
        if splitLine[0] == "Print Number":
            print_id = int(splitLine[1])

        # edition
        if splitLine[0] == "Edition":
            editionName = parseCompo(splitLine[1])
        if splitLine[0] == "Editor":
            editionAuthors = parseEditor(splitLine[1])


        # Composition
        if splitLine[0] == "Title": title = parseCompo(splitLine[1])
        if splitLine[0] == "Incipit": incipit = parseCompo(splitLine[1])
        if splitLine[0] == "Key": key = parseCompo(splitLine[1])
        if splitLine[0] == "Genre": genre = parseCompo(splitLine[1])
        if splitLine[0] == "Composition Year":
            compoYear = parseCompo(splitLine[1])
            if compoYear is not None and len(compoYear) == 4 : compoYear = int(compoYear)


        if splitLine[0] == "Partiture":
            partiture = parsePartiture(splitLine[1])
        if splitLine[0] == "Composer":
            for person in parsePerson(splitLine[1]):
                checker2 = False
                for item in personArray:
                    if person.name == item.name: checker2 = True
                if checker2 == False: personArray.append(person)
            #for person in parsePerson(splitLine[1]):
            #    if person.name not in personArray:
            #        personArray[person.name] = person
        if "Voice" in splitLine[0]:
            voice = parseVoice(splitLine[1])
            voiceArray.append(voice)


        if (lineBreak==True):
            # store Composition
            composition = (Composition(title, incipit, key, genre, compoYear, voiceArray, personArray))
            edition = Edition(editionName, composition, editionAuthors)
            printArray.append(Print(print_id, edition, partiture))
            voiceArray = []
            personArray = []
    return printArray



def parsePartiture(partiture):
        partiture = (partiture.strip())
        if (len(partiture)) == 0: outputPartiture = False
        if "yes" in partiture: outputPartiture = True
        if "no" in partiture: outputPartiture = False
        if "outputPartiture" not in locals():
            outputPartiture = False
        return outputPartiture


def parseEditor(editors):
    editorList = []
    editors = editors.strip(" ")
    try:
        if editors.find("(") != -1: editors = editors[:editors.find("(")]
    except:
        pass
    editors = editors.strip(" ")
    editors = editors.split(",")
    for index, item in enumerate(editors):
        item = item.strip(" ")
        subItem = item.split(" ")
        surname = subItem[len(subItem)-1]
        name = ""
        for i in range(0,len(subItem)-1):
            name += subItem[i] + " "
        editors[index] = item
        name = name.strip(" ")

        if name != "": editorList.append(Person(name + " " + surname, None, None))
        else:
            if surname != "": editorList.append(Person(surname, None, None))
    return editorList



def parseCompo(compoStuff):
        compoStuff = (compoStuff.strip())
        if len(compoStuff)==0 : compoStuff = None
        return compoStuff

def parseVoice(voice):
    name = ""
    range = ""
    voiceList = voice.split(",")
    # remove spaces
    for index, voice in enumerate(voiceList):
        voice = voice.strip()
        if "--" in voice:
            range = voice
        else:
            name += voice + ", "
    name = name.rstrip(", ")
    if range =="": range = None
    if name == "": name = None
    return (Voice(name,range))

def parsePerson(line):
    personList = (line.split(";"))
    personObject = []
    # remove spaces
    for index, person in enumerate(personList):
        person = person.strip()
        try:
            born,died = parseDate(person)
        except:
            pass
        if (re.search(r'\d', person)) is not None:
            person = person.split("(")[0]
            person = person.strip()
        checker = False
        for item in personObject:
            if (item.name==person): checker = True
        if checker==False:
            personObject.append(Person(person, born, died))
    return personObject

def parseDate(item):
    born = None
    died = None
    try:
        if item.find("+") != -1:
            died = item[item.find("+")+1:item.find("+")+5]
        if item.find("*") != -1:
            died = item[item.find("*")+1:item.find("*")+5]
        life = (re.search(r'\((.*?)\)',item).group(1))
        if life.find("--") != -1 and len(life) == 6 :
            born = life[:4]
            died = None
        if life.find("-") != -1 and len(life) == 5 :
            born = life[:4]
            died = None
        if life.find("--") != -1 and len(life) > 6: born,died = life.split("--")
        if life.find("-") != -1 and life.find("--") == -1 and len(life) > 5: born,died = life.split("-")

        if born is not None:
            born = born[:4]
            born = int(born)
        if died is not None:
            died = died[:4]
            died = int(died)
        return born, died
    except:
        return None,None

def returnStuff(item):
    returnValue = "Print Number: " + str(item.print_id) + "\n"

    composerReturn = ""
    for element in (item.edition.composition.authors):
        composer = ""
        composer += element.name
        if element.born is not None and element.died is not None:
            born = element.born
            died = element.died
            composer += " (" + str(element.born) + "--" + str(element.died) + "); "
        if element.born is not None and element.died is None:
            composer += " (" + str(element.born) + "--" + "); "
        if element.born is None and element.died is not None:
            composer += " (--" + str(element.died) + "); "
        if element.born is None and element.died is None: composer += "; "
        composerReturn += composer
    composerReturn= composerReturn.rstrip("; ")
    returnValue += "Composer: " + composerReturn + "\n"

    title = item.edition.composition.name
    if title is None: title = ""
    returnValue += "Title: " + title +"\n"

    genre = item.edition.composition.genre
    if genre is None: genre = ""
    returnValue += "Genre: " + genre + "\n"

    key = item.edition.composition.key
    if key is None: key = ""
    returnValue += "Key: " + key + "\n"

    compoYear = item.edition.composition.year
    if compoYear is None: compoYear = ""
    returnValue += "Composition Year: " + str(compoYear) + "\n"

    edition = item.edition.name
    if edition is None: edition = ""
    returnValue += "Edition: " + edition + "\n"

    author = ""
    for element in (item.edition.authors):
        author += element.name + ", "
    author = author.strip(", ")
    returnValue += "Editor: " + author + "\n"

    i = 1
    voice = ""
    for element in (item.edition.composition.voices):
        voice += "Voice " + str(i) + ": "
        if element.range is not None: voice += element.range + ", "
        if element.name is not None: voice += element.name + "\n"
        else: voice += "\n"
        i += 1
    returnValue += voice


    if item.partiture == True:
        partiture = "yes"
    else:
        partiture = "no"
    returnValue += "Partiture: " + partiture + "\n"

    incipit = item.edition.composition.incipit
    if incipit is None: incipit = ""
    returnValue += "Incipit: " + incipit

    return(returnValue)

class Print:
    def __init__(self, print_id, edition, partiture):
        self.print_id = print_id
        self.edition = edition
        self.partiture = partiture
    def composition(self):
        return self.edition.composition
    def format(self):
        return returnStuff(self)


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died


class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range

class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

class Edition:
    def __init__(self, name, composition, authors):
        self.name = name
        self.composition = composition
        self.authors = authors
