from wit import Wit

import mariadb
import asyncio
import difflib
import re


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
                "special topics":"CIS"}

classes = []
instructors = []
instructorsLastsNames = []
previousIntent = "None"
intent = "None"
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
    myCats = ["Computer Application","Programming","Information Security","Computer Network","Computer Engineering","Computing Theory","Special Topics"]
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

def getClassCode(name):
    code = name.replace(' ', '').upper()
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
                elif cate == 'special topics' and int(cla[0][3:7]) >= 4930: continue
                else: myNewList.append(cla)
    return myNewList


def getResponse(resp):
    global chosenCat
    global intent
    global previousIntent
    global className
    global profName
    global category
    if(intent == "professor"  or (previousIntent=="prereq" and intent=="wit$confirmation")):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False: return "Sorry, I did not get that"
        className = code
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

    elif intent == "wit$confirmation" and previousIntent == "greeting":
        return "Do you want to check out graduate level courses or undergraduate ones?"

    elif (previousIntent == "graduate" or previousIntent == "undergraduate") and intent == "dontknow":
        return "Courses are divided into the following categories. You can choose any and I can show you courses from that category. ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory"

    elif intent == "graduate" or intent == "undergraduate":
        chosenCat = intent
        res = 'Ok! ' + resp + 'And '
        if category == '':
            return res+"Which one of the following categories of courses are you looking for? ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory ==Special Topics"
        else:
            return res + f'Should I tell you about {category} courses?'
    elif intent == 'wit$negation' and previousIntent in ['graduate', 'undergraduate']:
            return "Which one of the following categories of courses are you looking for? ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory ==Special Topics"


    elif intent == "category" or (intent == 'wit$confirmation' and previousIntent in ['graduate', 'undergraduate']):
        temp = getCat(resp)
        if temp == False:
            resp = category
            if resp == '': return "Sorry, I did not get that."
        category = getCat(resp).lower()
        selectedClasses = getClassesFromCat(category)
        if(len(selectedClasses) > 3):
            res = f"The CISE department is offering {selectedClasses[0][1]}, {selectedClasses[1][1]}, {selectedClasses[2][1]} and {len(selectedClasses) - 3} other courses"
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            return res
        elif(len(selectedClasses) > 1):
            res = f"The CISE department is offering " + ", ".join([i[1] for i in selectedClasses])
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            return res
        elif(len(selectedClasses) == 1):
            res = f"The CISE department is offering {selectedClasses[0][1]}"
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            className = selectedClasses[0][0]
            return res
        elif(len(selectedClasses) == 0):
            res = f"The CISE department is not offering any {category} courses"

    elif(intent == "class_info"):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False:             return "Oh! There's no such course in the CISE department."
        className = code
        cursor.execute("select unique info from course WHERE code=? and name=?",(code,myTuple[1]))
        for info in cursor:
            return f"{myTuple[1]} covers {info[0]}. Would you like to know the class times?"

    elif(intent == "final_exam"):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False: return "Oh! There's no such course in the CISE department."
        className = code
        cursor.execute("select unique final from class where ccode=? and cname=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        finalDate = ''
        for final in ls:
            finalDate = final

        if(finalDate[0] != "--"):
            finalDate = parseFinalDate(finalDate[0])
            return f"The final exam for {myTuple[1]} will be on {finalDate}"
        else:
            return f"The final exam for {myTuple[1]} hasn't been set yet"

    elif(intent == "show_classes"):
        if chosenCat == '':
            return "Do you want to check out graduate level courses or undergraduate ones?"
        else:
            return f'Do you still want to checkout {chosenCat} level courses?'
    elif [previousIntent, intent] == ['show_classes', 'wit$confirmation']:
        intent = chosenCat
        return getResponse('')
    elif [previousIntent, intent] == ['show_classes', 'wit$negation']:
        intent = 'graduate' if chosenCat == 'undergraduate' else 'undergraduate'
        return getResponse(f'I will show {intent} courses. ')

    elif(intent == "textbook"):
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False: return "Oh! There's no such course in the CISE department."
        className = code
        cursor.execute("select text from course WHERE code=? and name=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        txt = ''
        for text in ls:
            txt = text[0]
        if(txt == ""):
            return f"You won't need any books for {myTuple[1]}"
        else:
            return f"You will need the book {txt} for {myTuple[1]}"

    elif(intent == "class_time" or (previousIntent == "class_info" and intent=="wit$confirmation")):

        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False: return "Oh! There's no such course in the CISE department."
        className = code
        cursor.execute("select unique location, day, btime, etime from class where ccode=? and cname=?",(code,myTuple[1]))
        ls = cursor.fetchall()
        if not ls: return f"{className} is not being offered in the upcoming semester."
        meetingTime = []
        for (location,day,btime,etime) in ls:
            meetingTime.append((location,day,str(btime)[:-3],str(etime)[:-3]))
        string = ""
        if(len(meetingTime) > 1 and meetingTime[0][1] != 'MWF'):
            string = f"{myTuple[1]} meets on {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} and {getDays(meetingTime[1][1])} from {meetingTime[1][2]} to {meetingTime[1][3]} at {meetingTime[0][0]}"

        elif(len(meetingTime) > 1 and meetingTime[0][1] == 'MWF'):
            string = f"{myTuple[1]} meets on {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} and {getDays(meetingTime[1][1])} from {meetingTime[1][2]} to {meetingTime[1][3]} at {meetingTime[0][0]}"

        else:
            string = f"{myTuple[1]} meets {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} at {meetingTime[0][0]}"

        intent = "class_time"
        return string + ". Would you like to know the prerequisites?"

    elif(intent == "prereq" or (previousIntent=="class_time" and intent=="wit$confirmation")):
        intent = "prereq"
        myTuple = getClassCode(resp)
        code = myTuple[0]
        if code == False:
            myTuple = getClassCode(className)
            code = myTuple[0]
            if code == False: return "Oh! There's no such course in the CISE department."
        className = code
        cursor.execute("select preq from course where code=? and name=?",(code,myTuple[1]))
        res = ''
        for (preq) in cursor:
            if(preq[0] == None):
                res = f"{myTuple[1]} does not have any prerequisites"
            else:
                res = f"The prerequisites for {myTuple[1]} are {preq[0]}"
        return res + '. And do you want know the instructor for this course?'

    elif intent == "show_professors":
        resp = str(len(instructors)) + " professors will be teaching classes next semester. Here is a list with all of them: "
        for i in instructors:
            resp += "=="+ str(i)
        return resp

    elif intent == "professor_classes":

        profName = getProffName(resp)
        if profName == False:
            myTuple = getProffName(profName)
            code = myTuple[0]
            if code == False:             return "Sorry, I didn't get that name."
        profName = code
        cursor.execute("select unique ccode,cname from class where instructor=?",(profName,))
        resp = f"{profName} is teaching "
        for (ccode,cname) in cursor:
            resp += cname + ", "
        # resp += ". Would you like to know their rating?"
        return resp
    elif [previousIntent, intent] == ["professor", "wit$confirmation"]:
        cursor.execute("select unique ccode,cname from class where instructor=?",(profName,))
        cs = [cname for (ccode, cname) in cursor]
        if len(cs) == 1:
            resp = f"Professor {profName} is not teaching any other courses this semester."
        else:
            resp = f"Professor {profName} is teaching " + 'and '.join(cs)
            # resp += ". Would you like to know their rating?"
        return resp

    elif previousIntent == "professor_classes" and intent == "wit$confirmation":
        intent = "professor_classes"
        proffName = getProffName(profName)
        if proffName == False:
            return "Oh! Something's wrong."
        cursor.execute("select rate from prof where name=?",(proffName,))
        for rate in cursor:
            if(rate == -1):
                return f"Oh! {proffName} does not have a rating"
            return f"{proffName} has a rating of {str(rate[0])} out of 5 on ratemyprofessors.com"

    elif intent == "wit$negation":
        return "Okay. I can help you find courses, their professor, final exam times, class meeting times, prerequisites and class information."

    elif intent == "thanks":
        return "Of course. I'm here to help!"

    # elif (previousIntent == "undergraduate" or previousIntent == "graduate") and (intent == "" or intent =="wit$negation"):
    #     return "Classes are divided into the following categories. You can choose any and I can show you classes from that category. ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory"

    elif intent == "bye":
        return "Pleasure to help you"

    else:
        print(previousIntent)
        print(intent)
        return "I'm sorry, I did not get that"

    return ""




getClasses();
getInstructors();

while(True):
    r = conn.recv(1024).decode()
    #if r != "": sio.emit('user_uttered', {"message": r})

    text = r
    # text = input("Enter message: ")
    print(text)
    if text != '':
        #with open('convo.txt', 'a') as f:
        #    f.write(r+'\n')
        response = client.message(text)
        previousIntent = intent
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
        print(previousIntent, intent, resp)
        msg = getResponse(resp) +'\n'
        print(msg)
        conn.send(msg.encode('utf-8'))
        #with open('convo.txt', 'a') as f:
        #    f.write(msg+'\n')
    if intent == "bye":
        break
conn.close()
    #tts = gTTS(text=getResponse(intent,className), lang="en")
    #tts.save("response.mp3")
    #os.system("response.mp3")()
    # engine.say(getResponse(intent,className))
    # engine.runAndWait()