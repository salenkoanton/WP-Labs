import json

class Fermer(object):
    def __init__(self, name = None, surname = None, age = None, square = None, birthday = None):
        self.name = name
        self.surname = surname
        self.age = age
        self.square = square
        self.birthday = birthday
    def parseFromDict(self, dict):
        self.__init__(dict.get("name"),dict.get("surname"),dict.get("age"),dict.get("square"),dict.get("birthday"))
        return self
    def toString(self):
        _str = ""
        _str += self.name + '\n'
        _str += self.surname + '\n'
        _str += str(self.age) + '\n'
        _str += str(self.square) + '\n'
        _str += self.birthday + '\n'*2
        return _str
    def toDict(self):
        return {'name' : self.name, 'surname' : self.surname, 'age' : self.age, 'square' : self.square, 'birthday' : self.birthday}




def parseFIle(filename):
    file = open(filename, "r")
    fermers = json.load(file);
    print (fermers)
    ferm_list = []
    for i in fermers:
        ferm_list.append(Fermer().parseFromDict(i))
    file.close()
    return ferm_list

def parseRequest(request):
    dictionary = {}
    if request.find('=') == -1:
        return None
    for s in request.split('&'):
        arglist = s.split('=', 1)
        print (arglist);
        dictionary.update({arglist[0] : arglist[1]})
    print (dictionary)
    return dictionary
#while True:
#    value = int(input('enter age value'))
#    data = parse("Fermers.json")
#    newdata = []
#    for i in data:
#        if i.age > value:
#    outstr = ''
#    for i in newdata:
#        outstr += i.toString()
#    print(outstr)
def getJson(request):
    if request == "all":
        file = open("Fermers.json", "r")
        fermers = json.load(file);
        return json.dumps(fermers, sort_keys=True, indent=4)

    argdict = parseRequest(request)
    if argdict == None:
        return '[{"exception" : "wrong args"}]'
    fermlist = parseFIle("Fermers.json")
    newFermList = fermlist.copy()
    for fermer in fermlist:
        for key, value in argdict.items():
            if key == "name":
                if fermer.name != value:
                    print("name")
                    newFermList.remove(fermer)
                    break
            elif key == "surname":
                if fermer.surname != value:
                    print("surname")
                    newFermList.remove(fermer)
                    break
            elif key[-2:] == 'lt':
                if key.find("age") == 0:
                    if fermer.age >= int(value):
                        print("agelt")
                        newFermList.remove(fermer)
                        break
                elif key.find("square") == 0:
                    if fermer.square >= float(value):
                        print("squarelt")
                        newFermList.remove(fermer)
                        break
            elif key[-2:] == 'gt':
                if key.find("age") == 0:
                    if fermer.age <= int(value):
                        print("agegt" + fermer.name)
                        newFermList.remove(fermer)
                        break
                elif key.find("square") == 0:
                    if fermer.square <= float(value):
                        print("squaregt")
                        newFermList.remove(fermer)
                        break

            elif key == "age":
                if fermer.age != int(value):
                    print("age")
                    newFermList.remove(fermer)
                    break
            elif key == "square":
                if fermer.square != float(value):
                    print("square")
                    newFermList.remove(fermer)
                    break
            else:
                return '[{"exception" : "wrong args"}]'
    returnList = []
    for fermer in newFermList:
        print(fermer.toString())
        returnList.append(fermer.toDict())
    return json.dumps(returnList, sort_keys=True, indent=4)
#print(getJson("agegt=100&squarelt=100"))
