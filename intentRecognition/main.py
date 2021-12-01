from wit import Wit

import mariadb
import asyncio
import difflib
import os


from threading import Thread
from socket import *
import socketio
import sys

#ip = sys.argv[1]
#port = int(sys.argv[2])
#s = socket(AF_INET, SOCK_STREAM)
#s.bind((ip, port))
#s.listen(1)
#conn, addr = s.accept()
#print("Connected: ", addr)


def send(msg):
    conn.send(msg.encode())


client = Wit("KADJWIX3VLFUEXI6DD5GFNWMVWI6FZBV")
connection = mariadb.connect(user='shiv', password='bang', database='soc', host='localhost')
cursor = connection.cursor()
chosenCat = 1

months = ["january","february","march","april","may","june","july","august","september","october","november","december",]
classPeriods = {"1":"from 7:25am to 8:15am",
                "2":"from 8:30am to 9:20am",
                "3":"from 9:35am to 10:25am",
                "4":"from 10:40am to 11:30am",
                "5":"from 11:45am to 12:35pm",
                "6":"from 12:50pm to 1:40pm",
                "7":"from 1:55pm to 2:45pm",
                "8":"from 3:00pm to 3:50pm",
                "9":"from 4:05pm to 4:55pm",
                "10":"from 5:10pm to 6:00pm",
                "11":"from 6:15pm to 7:05pm",
                "E1":"from 7:20pm to 8:10pm",
                "E2":"from 8:20pm to 9:10pm",
                "E3":"from 9:20pm to 10:10pm"}

categories = {"computer application":"CAP",
                "programming":"COP",
                "information security":"CIS",
                "computer network":"CNT",
                "computer engineering":"CEN",
                "computing theory":"COT"}

classes = []
instructors = []
instructorsLastsNames = []
previousIntent = "None"
intent = "None"

def textInput():
    return str(input("Please enter your text: "))


def getClasses():
    cursor.execute("select unique ccode,cname from class;")
    for (ccode,cname) in cursor:
        classes.append((ccode,cname))

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
    if day == "MWF":
        return "mondays wednesdays and fridays"
    elif day == "T":
        return "tuesday"
    elif day == "R":
        return "thursday"


def getCat(name):
    myCats = ["Computer Application","Programming","Information Security","Computer Network","Computer Engineering","Computer Theory"]
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
    if any(char.isdigit() for char in name):
        code = name.upper()
        classes2 = []
        for i in classes:
            classes2.append(i[0])
        courseCode = difflib.get_close_matches(name,classes2)
        if(len(courseCode) == 0):
            return (False,False)
        courseCode = courseCode[0]
        for i in classes:
            if i[0] == courseCode:
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
            if(chosenCat == 1):
                if(i[1] == courseName and int(i[0][3:7]) >= 5000):
                    return i
            elif(chosenCat == 0):
                if(i[1] == courseName and int(i[0][3:7]) < 5000):
                    return i

    return (False,False)


def getClassesFromCat(cat):
    myNewList = []
    global chosenCat
    for cla in classes:
        if(chosenCat == 1):
            if(cla[0][0:3] == cat and int(cla[0][3:7]) >= 5000):
                myNewList.append(cla)
        elif(chosenCat == 0 and int(cla[0][3:7]) < 5000):
            if(cla[0][0:3] == cat):
                myNewList.append(cla)
    return myNewList


def getResponse(className):
    global chosenCat
    global intent
    global previousIntent
    if(intent == "professor"):
        myTuple = getClassCode(className)
        code = myTuple[0]
        if code == False:
            return "Sorry, I did not get that"
        cursor.execute("select unique instructor from class where ccode=? and cname=?",(code,myTuple[1]))
        for instructor in cursor:
            return f"Professor {instructor[0]} will be teaching {myTuple[1]}. Would you like to know the meeting times?"

    elif intent == "greeting":
        return "Hi! I'm Vicky. Would you like me to help you select courses for the upcoming semester?"

    elif previousIntent == "greeting" and intent == "":
        return "Okay. I'm always here if you need help with classes in the future."

    elif intent == "wit$confirmation" and previousIntent == "greeting":
        return "Do you want to check out graduate level courses or undergraduate ones?"

    elif (previousIntent == "graduate" or previousIntent == "undergraduate") and intent == "dontknow":
        return "Classes are divided into the following categories. You can choose any and I can show you classes from that category. ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory"

    elif intent == "graduate":
        chosenCat = 1
        return "Which one of the following categories of courses are you looking for? ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory"

    elif intent == "undergraduate":
        chosenCat = 0
        return "Which one of the following categories of courses are you looking for? ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory"

    elif intent == "category":
        temp = getCat(className)
        if temp == False:
            return "Sorry, I did not get that."
        category = categories[getCat(className).lower()]
        selectedClasses = getClassesFromCat(category)
        if(len(selectedClasses) > 3):
            res = f"The CISE department is offering {selectedClasses[0][1]}, {selectedClasses[1][1]}, {selectedClasses[2][1]} and {len(selectedClasses) - 3} other classes"
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            return res
        elif(len(selectedClasses) > 0):
            res = f"The CISE department is offering {selectedClasses[0][1]} and {selectedClasses[1][1]} "
            for i in selectedClasses:
                res += "=="+ str(i[0]) + " - " + str(i[1])
            return res
        elif(len(selectedClasses) == 0):
            res = f"The CISE department is not offering any classes in {category}"


    elif(intent == "class_info"):
        myTuple = getClassCode(className)
        code = myTuple[0]
        if code == False:
            return "Sorry, I did not get that"
        cursor.execute("select unique info from course WHERE code=? and name=?",(code,myTuple[1]))
        for info in cursor:
            return f"{myTuple[1]} covers {info[0]}. Would you like to know the meeting times?"


    elif(intent == "final_exam"):
        myTuple = getClassCode(className)
        code = myTuple[0]
        if code == False:
            return "Sorry, I did not get that"
        cursor.execute("select unique final from class where ccode=? and cname=?",(code,myTuple[1]))
        finalDate = ""
        for final in cursor:
            finalDate = final

        if(finalDate[0] != "--"):
            finalDate = parseFinalDate(finalDate[0])
            return f"The final exam for {myTuple[1]} will be on {finalDate}"
        else:
            return f"The final exam for {myTuple[1]} hasn't been set yet"

    elif(intent == "show_classes"):
        return "Do you want to check out graduate level courses or undergraduate ones?"

    elif(intent == "textbook"):
        return "Here are the textbooks you will need for " + className

    elif(intent == "class_time" or (previousIntent == "class_info" and intent=="wit$confirmation") or (previousIntent == "professor" and intent=="wit$confirmation")):

        myTuple = getClassCode(className)
        code = myTuple[0]
        if code == False:
            return "Sorry, I did not get that"
        cursor.execute("select unique location, day, btime, etime from class where ccode=? and cname=?",(code,myTuple[1]))
        meetingTime = []
        for (location,day,btime,etime) in cursor:
            meetingTime.append((location,day,btime,etime))

        string = ""
        if(len(meetingTime) > 1 and meetingTime[0][1] != 'MWF'):
            string = f"{myTuple[1]} meets on {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} and {getDays(meetingTime[1][1])} from {meetingTime[1][2]} to {meetingTime[1][3]} at {meetingTime[0][0]}"

        elif(len(meetingTime) > 1 and meetingTime[0][1] == 'MWF'):
            string = f"{myTuple[1]} meets on {getDays(meetingTime[0][1])} from {meetingTime[0][2]} to {meetingTime[0][3]} and {getDays(meetingTime[1][1])} from {meetingTime[1][2]} to {meetingTime[1][3]} at {meetingTime[0][0]}"

        else:
            string = f"{className} meets {getDays(day)} from {btime} to {etime} at {location}"

        intent = "class_time"
        return string + ". Would you like to know the prerequisites?"

    elif(intent == "prereq" or (previousIntent=="class_time" and intent=="wit$confirmation")):
        intent = "prereq"
        myTuple = getClassCode(className)
        code = myTuple[0]
        if code == False:
            return "Sorry, I did not get that"
        cursor.execute("select preq from course where code=? and name=?",(code,myTuple[1]))
        for (preq) in cursor:
            if(preq[0] == None):
                return f"{myTuple[1]} does not have any pre requisites"
            else:
                return f"The prerequisites for {myTuple[1]} are {preq[0]}"

    elif intent == "show_professors":
        resp = str(len(instructors)) + " professors will be teaching classes next semester. Here is a list with all of them: "
        for i in instructors:
            resp += "=="+ str(i)
        return resp

    elif intent == "professor_classes":

        proffName = getProffName(className)
        if proffName == False:
            return "Sorry, I didn't get that name. Please say the full name"
        cursor.execute("select unique ccode,cname from class where instructor=?",(proffName,))
        resp = f"{proffName} is teaching "
        for (ccode,cname) in cursor:
            resp += cname + " "
        resp += ". Would you like to know their rating?"
        return resp

    elif previousIntent == "professor_classes" and intent == "wit$confirmation":
        intent = "professor_classes"
        proffName = getProffName(className)
        if proffName == False:
            return "Sorry, I didn't get that name."
        return f"{proffName} is rated 3.5 out of 5"

    elif (previousIntent == "professor_classes" and intent == "wit$negation") or intent == "wit$negation":
        return "Okay. I can help you find classes, their professor, final exam times, meeting times, prerequisites and class information. Just ask me to show you classes!"

    elif intent == "thanks":
        return "Of course. I'm here to help!"
    elif (previousIntent == "undergraduate" or previousIntent == "graduate") and intent == "":
        return "Classes are divided into the following categories. You can choose any and I can show you classes from that category. ==Computer Application ==Programming ==Information Security ==Computer Network ==Computer Engineering ==Computing Theory""
    else:
        print(previousIntent)
        print(intent)
        return "Im sorry, I did not get that"

    return ""




def init():
    getClasses();
    getInstructors();

    className = None
    while(True):
        #r = conn.recv(1024).decode()
        #if r != "": sio.emit('user_uttered', {"message": r})

        #text = r
        text = input("Enter message: ")
        print(text)
        if text != '':
            #with open('convo.txt', 'a') as f:
            #    f.write(r+'\n')
            response = client.message(text)
            global previousIntent
            global intent
            previousIntent = intent
            if (len(response["intents"]) == 0):
                intent = ""
            else:
                intent = response["intents"][0]["name"]
            if(response["entities"] and intent != 'wit$confirmation'):
                try:
                    className = str(response["entities"]["class_name:class_name"][0]["value"])
                except:
                    className = str(response["entities"]["professor_name:professor_name"][0]["value"])

            msg = getResponse(className) +'\n'
            print(msg)
            #conn.send(msg.encode('utf-8'))
            #with open('convo.txt', 'a') as f:
            #    f.write(msg+'\n')
        if intent == "Bye":
            break
    #conn.close()
        #tts = gTTS(text=getResponse(intent,className), lang="en")
        #tts.save("response.mp3")
        #os.system("response.mp3")()
        # engine.say(getResponse(intent,className))
        # engine.runAndWait()


init()
