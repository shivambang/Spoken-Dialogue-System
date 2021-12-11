from wit import Wit

import mariadb
import asyncio
import difflib
import re
from datetime import datetime

from threading import Thread
from socket import *
# import socketio
import sys

ip = sys.argv[1]
port = int(sys.argv[2])
s = socket(AF_INET, SOCK_STREAM)
s.bind((ip, port))
s.listen(1)
conn, addr = s.accept()
print("Connected: ", addr)


def send(msg):
    conn.send(msg.encode())


client = Wit("KADJWIX3VLFUEXI6DD5GFNWMVWI6FZBV")
connection = mariadb.connect(user='shiv', password='bang', database='soc', host='localhost')
cursor = connection.cursor()

months = ["january","february","march","april","may","june","july","august","september","october","november","december",]
categories = {"computer application":"CAP",
                "programming":"COP",
                "information security":"CIS",
                "computer network":"CNT",
                "computer engineering":"CEN",
                "computing theory":"COT",
                "computer design":"CDA",
                "special topics":"CIS"}
desc = {"computer application":"Courses related to application of computer science principles such as Machine Learning, Human Computer Interaction, Computer Graphics..",
        "programming":"Courses related to programming principles such as Database Management Systems, Data Structures, PROGRAMMING LANGUAGE PRINCIPLES..",
        "information security":"Topics related to information and security in computer science such as Cryptology, Enterprise Security..",
        "computer network":"Courses related to networking principles in computer science..",
        "computer engineering":"Engineering related computer science courses such as Software Engineering, Software Testing..",
        "computing theory":"Theoritical courses in computer science such as Numerical Analysis, Analysis of Algorithms..",
        "computer design":"Computer Design and Architecture courses such as Embedded Systems..",
        "special topics":"Elective Courses with topics of current significance in computer science.."}

classes = []
instructors = []
instructorsLastsNames = []
intentArr = ['NA', 'NA', 'NA', 'NA', 'NA']
classCode = ''
className = ''
profName = ''
chosenCat = ''
category = ''
def reset():
    global intentArr, classCode, className, profName, chosenCat, category

    intentArr = ['NA', 'NA', 'NA', 'NA', 'NA']
    classCode = ''
    className = ''
    profName = ''
    chosenCat = ''
    category = ''

def textInput():
    return str(input("Please enter your text: "))


def getClasses():
    cursor.execute("select code,name,last from course;")
    for (code,name,last) in cursor:
        classes.append((code,name,last))

def getInstructors():
    cursor.execute("select unique instructor from class;")
    for instructor in cursor:
        instructors.append(instructor[0])
        #instructorsLastsNames.append(instructor[0].split(" ")[1])

def findByLastName(last):
    for i in instructors:
        if last == i.split(" ")[1]:
            return i
    return False

def parseFinalDate(final):
    firstSplit = final.split("@")
    secondSplit = firstSplit[1].split("-")
    return months[int(firstSplit[0].split("/")[0])] + " " + firstSplit[0].split("/")[1] + " of " + firstSplit[0].split("/")[2] + "from" + secondSplit[0] + " to" + secondSplit[1]

def getDays(day):
    days = []
    for d in day:
        if d == 'M':
            days.append('Monday')
        elif d == 'T':
            days.append('Tuesday')
        elif d == 'W':
            days.append('Wednesday')
        elif d == 'R':
            days.append('Thursday')
        elif d == 'F':
            days.append('Friday')
    return ', '.join(days)


def getCat(name):
    myCats = ["Computer Application","Programming","Information Security","Computer Network","Computer Engineering","Computer Design","Computing Theory","Special Topics"]
    courseName = difflib.get_close_matches(name,myCats)
    if(len(courseName) == 0):
        return False
    courseName = courseName[0]
    return courseName

def getProffName(proff):
    proffName = difflib.get_close_matches(proff,instructors)
    if(len(proffName) == 0):
        #proffName = difflib.get_close_matches(proff,instructorsLastsNames)
        #if(len(proffName) == 0):
        #    return False
        #proffName = proffName[0]
        #return findByLastName(proffName)
        return False
    proffName = proffName[0]
    return proffName

def getCode(name):
    num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    tokens = name.replace('sea', 'c').split(' ')
    code = ''
    for i in range(len(tokens)):
        if len(code) >= 3:
            tokens = tokens[i:]
            break
        code += tokens[i]
    for i in range(len(tokens)):
        try:
            int(tokens[i])
            code += tokens[i]
        except:
            n = difflib.get_close_matches(tokens[i], num)
            if len(n) > 0:
                code += str(num.index(n[0]))
    print(code)
    return code
def getClassCode(name):
    code = getCode(name.lower()).upper()
    if re.match('[A-Z]{3}[0-9]{4}', code):
        classes2 = []
        # for i in classes:
        #     classes2.append(i[0])
        # courseCode = difflib.get_close_matches(code,classes2)
        # if(len(courseCode) == 0):
        #     return (False,False)
        # courseCode = courseCode[0]
        for i in classes:
            if i[0] == code:
                return i
    else:
        classes2 = []
        for i in classes:
            classes2.append(i[1])
        courseName = difflib.get_close_matches(name,classes2)
        if(len(courseName) == 0):
            return (False,False)
        courseName = courseName[0]
        for i in classes:
            #if(chosenCat == 1):
            #    if(i[1] == courseName and int(i[0][3:7]) >= 5000):
            #        return i
            #elif(chosenCat == 0):
            #    if(i[1] == courseName and int(i[0][3:7]) < 5000):
            #        return i
            if(i[1] == courseName):
                return i

    return (False,False)


def getClassesFromCat(cate):
    myNewList = []
    global chosenCat
    cat = categories[cate]
    for cla in classes:
        if cla[2].upper() == 'N22': continue
        if(chosenCat == "graduate"):
            if(cla[0][0:3] == cat[0:3] and int(cla[0][3:7]) >= 5000):
                if cate == 'information security' and int(cla[0][3:7]) >= 6900: continue
                elif cate == 'special topics' and int(cla[0][3:7]) != 6930: continue
                else: myNewList.append(cla)
        elif(chosenCat == "undergraduate"):
            if(cla[0][0:3] == cat[0:3] and int(cla[0][3:7]) < 5000):
                if cate == 'information security' and int(cla[0][3:7]) >= 4900: continue
                elif cate == 'special topics' and int(cla[0][3:7]) != 4930: continue
                else: myNewList.append(cla)
    return myNewList


def getResponse(resp, prev=''):
    global chosenCat
    global intentArr
    global classCode
    global className
    global profName
    global category
    intent = intentArr[4]
    previousIntent = intentArr[3]
    if(intent == "professor"  or (previousIntent=="textbook" and intent=="wit$confirmation")):
        if intent != "professor":
            intentArr.append('professor')
            intentArr = intentArr[1:]
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False: return "Oh! I couldn't find that course."
        className = myTuple[1]
        cursor.execute("select unique instructor from class where ccode=? and cname=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        for instructor in ls:
            profName = instructor[0]
            return f"{myTuple[1]} will be taught by Professor {profName}. Would you like to know what other courses they would be teaching?"
        
    elif intent == "greeting":
        return "Hi! I'm Vicky. Would you like me to help you select courses for the upcoming semester?"

    elif previousIntent == "greeting" and intent == "":
        return "Okay. I'm always here if you need help in the future."

    elif (intent == "wit$confirmation" and previousIntent == "greeting"):
        return "Do you want to check out graduate level courses or undergraduate ones?"

    elif intent == "graduate" or intent == "undergraduate":
        chosenCat = intent
        res = 'Ok! ' + prev + 'And '
        resp = '' if not getCat(resp) else getCat(resp)
        if resp == '':
            if category == '':
                return res+"Which one of the following categories of courses are you looking for? ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computer Design ==Computing Theory ==Special Topics"
            else:
                return res + f'you want to see {category} courses. Is that correct?'
        else:
            intentArr.append('category')
            intentArr = intentArr[1:]
            return getResponse(resp)
    elif intent == 'wit$negation' and previousIntent in ['graduate', 'undergraduate']:
            return "Which one of the following categories of courses are you looking for? ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computer Design ==Computing Theory ==Special Topics"

    elif (intent == "dncat") or ((previousIntent == chosenCat or intentArr[2:-1] == [chosenCat, 'wit$negation']) and intent == "dontknow"):
        if intent != 'dncat':
            intentArr.append('dncat')
            intentArr = intentArr[1:]
        return "Would you like to know more about the categories?"

    elif intentArr[3:] == ['category', 'wit$confirmation']:
        if resp:
            cn = getClassCode(resp)
            code = cn[0]
            if code == False: return "Oh! I couldn't find that."
            className = cn[1]
        if className: 
            intentArr.append('class_info')
            intentArr = intentArr[1:]
            return getResponse(className)
        return "Ok, which course would you like to know more about?"
    elif (intent == "class_info") or (intentArr[2:-1] == ['category', 'wit$confirmation'] and intent in ['category', 'class_info']):
        if resp == '':
            if previousIntent == 'graduate':
                intentArr[-1] = 'dncat'
                return getResponse('')
            cn = getClassCode(className)
            code = cn[0]
            if code == False:
                intentArr[-1] = 'fail_info'
                return "Oh! I couldn't find that course. Would you like to see the available courses?"
        else:             
            cn = getClassCode(resp)
            ct = getCat(resp)
            code = cn[0]
            if not (difflib.SequenceMatcher(None, resp, str(cn[0])).quick_ratio() >= difflib.SequenceMatcher(None, resp, str(ct)).quick_ratio() or difflib.SequenceMatcher(None, resp, str(cn[1])).quick_ratio() >= difflib.SequenceMatcher(None, resp, str(ct)).quick_ratio()):
                print(resp, cn[1], ct)
                intentArr[-1] = 'getcat'
                return getResponse(resp)
            if code == False:
                if previousIntent == 'graduate':
                    intentArr[-1] = 'dncat'
                    return getResponse('')
                intentArr[-1] = 'fail_info'
                return "Oh! I couldn't find that course. Would you like to see the available courses?"
        className = cn[1]
        res = ''
        cursor.execute("select unique info from course WHERE code=? and name=?",(code,cn[1]))
        for info in cursor:
            res = f"{cn[0]} ({cn[1]}) {info[0]}"
        if intent != "class_info":
            intentArr.append('class_info')
            intentArr = intentArr[1:]
        return res + '. Would you like to know the class times?'

    elif intentArr[3:] == ['dncat', 'wit$confirmation']:
        return "Ok, which category would you like to know more about?"
    elif intent == 'getcat' or (intentArr[2:-1] == ['dncat', 'wit$confirmation'] and intent in ['category', 'class_info']):
        intentArr[4] = 'getcat'
        temp = getCat(resp)
        if temp == False:
            if resp == '': return "Oh! Something's not right! Were you looking for graduate level courses or undergraduate ones?"
        className = ''
        category = getCat(resp).lower()
        res = category + " covers " + desc[category]
        # selectedClasses = getClassesFromCat(category)
        # if(len(selectedClasses) > 3):
        #     res += f" The CISE department is offering {selectedClasses[0][1]}, {selectedClasses[1][1]}, {selectedClasses[2][1]} and {len(selectedClasses) - 3} other courses"
        #     res += '. Would you like to know more about any of these courses?'
        #     for i in selectedClasses:
        #         res += "=="+ str(i[0]) + " - " + str(i[1])

        # elif(len(selectedClasses) > 1):
        #     res += f" The CISE department is offering " + ", ".join([i[1] for i in selectedClasses])
        #     res += '. Would you like to know more about any of these courses?'
        #     for i in selectedClasses:
        #         res += "=="+ str(i[0]) + " - " + str(i[1])

        # elif(len(selectedClasses) == 1):
        #     res += f" The CISE department is offering {selectedClasses[0][1]}"
        #     res += '. Would you like to know more about that course?'
        #     for i in selectedClasses:
        #         res += "=="+ str(i[0]) + " - " + str(i[1])
        #     className = selectedClasses[0][0]

        # elif(len(selectedClasses) == 0):
        #     res += f" The CISE department is not offering any {category} courses"
        return res + f'. Would you like to know the {category} courses being offered?'

    elif intent == "category" or (intent == 'wit$confirmation' and previousIntent in ['graduate', 'undergraduate', 'getcat']):
        if intent != "category":
            intentArr.append('category')
            intentArr = intentArr[1:]
        temp = getCat(resp)
        if temp == False:
            resp = category
            if resp == '': return "Oh! Something's not right! Were you looking for graduate level courses or undergraduate ones?"
        className = ''
        category = getCat(resp).lower()
        if chosenCat == '': return "Oh! Something's not right! Were you looking for graduate level courses or undergraduate ones?"
        selectedClasses = getClassesFromCat(category)
        if(len(selectedClasses) > 3):
            res = f"The CISE department is offering {selectedClasses[0][1]}, {selectedClasses[1][1]}, {selectedClasses[2][1]} and {len(selectedClasses) - 3} other {category} courses"
            res += '. Would you like to know more about any of these courses?'
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            return res
        elif(len(selectedClasses) > 1):
            res = f"The CISE department is offering " + ", ".join([i[1] for i in selectedClasses])
            res += '. Would you like to know more about any of these courses?'
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            return res
        elif(len(selectedClasses) == 1):
            res = f"The CISE department is offering {selectedClasses[0][1]}"
            res += '. Would you like to know more about that course?'
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            className = selectedClasses[0][0]
            return res
        elif(len(selectedClasses) == 0):
            res = f"The CISE department is not offering any {category} courses"
            return res

    elif(intent == "final_exam"):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False:
                intentArr[-1] = 'fail_info'
                return "Oh! I couldn't find that course. Would you like to see the available courses?"
        className = myTuple[1]
        cursor.execute("select unique final from class where ccode=? and cname=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        finalDate = ''
        for final in ls:
            finalDate = final

        if(finalDate[0] != "--"):
            finalDate = parseFinalDate(finalDate[0])
            return f"The final exam for this course will be on {finalDate}"
        else:
            return f"The final exam for this course hasn't been set yet"

    elif(intent == "show_classes") or (intent == 'wit$confirmation' and previousIntent == 'fail_info'):
        if intent != "show_classes":
            intentArr.append('show_classes')
            intentArr = intentArr[1:]
        if chosenCat == '':
            return "Do you want to check out graduate level courses or undergraduate ones?"
        else:
            return f'Do you still want to checkout {chosenCat} level courses?'
    elif [previousIntent, intent] == ['show_classes', 'wit$confirmation']:
        intent = chosenCat
        intentArr.append(intent)
        intentArr = intentArr[1:]
        return getResponse('')
    elif [previousIntent, intent] == ['show_classes', 'wit$negation']:
        intent = 'graduate' if chosenCat == 'undergraduate' else 'undergraduate'
        intentArr.append(intent)
        intentArr = intentArr[1:]
        return getResponse('', f'I will show {intent} courses. ')

    elif(intent == "textbook") or (previousIntent=="prereq" and intent=="wit$confirmation"):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False:
                intentArr[-1] = 'fail_info'
                return "Oh! I couldn't find that course. Would you like to see the available courses?"
        className = myTuple[1]
        cursor.execute("select text from course WHERE code=? and name=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        txt = ''
        for text in ls:
            txt = text[0]
        res = ''
        if(txt == ""):
            res = f"You won't need any textbooks for this course"
        else:
            res = f"You will need the textbook {txt} for this course"
        if intent != "textbook":
            intentArr.append('textbook')
            intentArr = intentArr[1:]
            return res + '. And would you like to know who would be teaching it?'
        else: return res

    elif(intent == "class_time" or (previousIntent == "class_info" and intent=="wit$confirmation")):

        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False:
                intentArr[-1] = 'fail_info'
                return "Oh! I couldn't find that course. Would you like to see the available courses?"
        className = myTuple[1]
        cursor.execute("select unique location, day, btime, etime from class where ccode=? and cname=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        meetingTime = []
        for (location,day,btime,etime) in ls:
            meetingTime.append((location,day,str(btime)[:-3],str(etime)[:-3]))
        string = ""
        if(len(meetingTime) > 1 and meetingTime[0][1] != 'MWF'):
            string = f"{myTuple[0]} meets on {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} and {getDays(meetingTime[1][1])} from {meetingTime[1][2]} to {meetingTime[1][3]} at {meetingTime[0][0]}"

        elif(len(meetingTime) > 1 and meetingTime[0][1] == 'MWF'):
            string = f"{myTuple[0]} meets on {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} and {getDays(meetingTime[1][1])} from {meetingTime[1][2]} to {meetingTime[1][3]} at {meetingTime[0][0]}"

        else:
            string = f"{myTuple[0]} meets {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} at {meetingTime[0][0]}"

        if intent != "class_time":
            intentArr.append('class_time')
            intentArr = intentArr[1:]
            return string + ". Do you want to know the prerequisites?"
        else: return string

    elif(intent == "prereq" or (previousIntent=="class_time" and intent=="wit$confirmation")):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False:
                intentArr[-1] = 'fail_info'
                return "Oh! I couldn't find that course. Would you like to see the available courses?"
        className = myTuple[1]
        cursor.execute("select preq from course where code=? and name=?",(code,myTuple[1]))
        res = ''
        for (preq) in cursor:
            if(preq[0] == None):
                res = f"{myTuple[1]} does not have any prerequisites"
            else:
                res = f"The prerequisites for {myTuple[1]} are {preq[0]}"
        if intent != "prereq":
            intentArr.append('prereq')
            intentArr = intentArr[1:]
            return res + '. Do you want to know the required textbooks for this course?'
        else: return res

    elif intent == "show_professors":
        resp = str(len(instructors)) + " professors will be teaching classes next semester. Here is a list with all of them: "
        for i in instructors:
            resp += "=="+ str(i)
        return resp

    elif intent == "professor_classes" or [previousIntent, intent] == ["professor", "wit$confirmation"]:

        pn = getProffName(resp)
        if pn == False:
            if previousIntent == 'professor': pn = getProffName(profName)
            if pn == False:             return "Oh! I don't recognize that name."
        profName = pn
        cursor.execute("select unique ccode,cname from class where instructor=?",(profName,))
        cs = [cname for (ccode, cname) in cursor]
        if len(cs) == 1 and intent != 'professor_classes':
            resp = f"Professor {profName} is not teaching any other courses next semester."
        else:
            resp = f"Professor {profName} will be teaching " + ' and '.join(cs)
            # resp += ". Would you like to know their rating?"
        return resp

    elif intent == "prof_rate":
        pn = getProffName(resp)
        if pn == False:
            pn = getProffName(profName)
            if pn == False:             return "Oh! I don't recognize that name."
        profName = pn
        cursor.execute("select rate from prof where name=?",(profName,))
        for rate in cursor:
            if(rate == -1):
                return f"Oh! {profName} does not have a rating"
            return f"{profName} has a rating of {str(rate[0])} out of 5 on ratemyprofessors.com"

    elif intent == "wit$negation" or intent == 'wit$confirmation':
        # return "Okay. I can help you find courses, their professor, final exam date, class meeting times, prerequisites and class information."
        return 'Okay. I can help you find courses, their professor, final exam date, class meeting times, prerequisites and class information.'


    elif intent == "thanks":
        return "Of course. I'm here to help!"

    # elif (previousIntent == "undergraduate" or previousIntent == "graduate") and (intent == "" or intent =="wit$negation"):
    #     return "Classes are divided into the following categories. You can choose any and I can show you classes from that category. ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory"

    elif intent == "bye":
        return "Pleasure to help you"
    elif intent == "bot":
        return "I can help you find courses, their professor, final exam date, class meeting times, prerequisites and class information."

    else:
        print(previousIntent)
        print(intent)
        return "I'm sorry, I didn't get that."

    return ""




getClasses();
getInstructors();
f = open('bc.txt', 'a')
while(True):
    r = conn.recv(1024).decode()
    #if r != "": sio.emit('user_uttered', {"message": r})

    text = r
    # text = input("Enter message: ")
    print(text, file=f, flush=True)
    print(text)
    if text == '/restart': break
    if text != '':
        #with open('convo.txt', 'a') as f:
        #    f.write(r+'\n')
        response = client.message(text)
        if (len(response["intents"]) == 0):
            intent = ""
        else:
            intent = response["intents"][0]["name"]
        resp = ''
        if(response["entities"] and intent != 'wit$confirmation' and intent != "wit$negation"):
            try:
                resp = str(response["entities"]["class_name:class_name"][0]["value"])
                # className = ent if ent != '' else className
            except:
                resp = str(response["entities"]["professor_name:professor_name"][0]["value"])
                # profName = ent if ent != '' else profName
        if intent == 'greeting': print('Hello', datetime.now(), file=f, flush=True)
        if intent == '': 
            if resp: msg = getResponse(resp) +'\n'
            else: msg = "I'm sorry, I didn't get that.\n"
        else:
            intentArr.append(intent)
            intentArr = intentArr[1:]
            msg = getResponse(resp) +'\n'
        print(intentArr, resp, file=f, flush=True)
        print(msg, file=f, flush=True)
        print(intentArr, resp)
        print(msg)
        conn.send(msg.encode('utf-8'))
        #with open('convo.txt', 'a') as f:
        #    f.write(msg+'\n')
    if intent == "bye":
        reset()
        print('Bye', datetime.now(), file=f, flush=True)
conn.close()
f.close()
    #tts = gTTS(text=getResponse(intent,className), lang="en")
    #tts.save("response.mp3")
    #os.system("response.mp3")()
    # engine.say(getResponse(intent,className))
    # engine.runAndWait()