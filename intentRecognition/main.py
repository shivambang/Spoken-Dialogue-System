from wit import Wit
import pyttsx3
import mariadb
from gtts import gTTS
import os




client = Wit("KADJWIX3VLFUEXI6DD5GFNWMVWI6FZBV")
connection = mariadb.connect(user='shiv', password='bang', database='soc', host='localhost')
cursor = connection.cursor()
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

def textInput():
    return str(input("Please enter your text: "))


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

def getResponse(intent, className):
    if(intent == "professor"):
        cursor.execute("SELECT unique instructor FROM class WHERE ccode LIKE CONCAT(?,'%') OR cname LIKE CONCAT(?,'%')",(className,className))
        for instructor in cursor:
            return f"Professor: {instructor} will be teaching {className}"
    elif(intent == "class_info"):
        cursor.execute("select unique info from course WHERE code=? OR name=?",(className,className))
        for info in cursor:
            return f"{className} covers {info}"
    elif(intent == "final_exam"):
        cursor.execute("select unique final from class where ccode LIKE CONCAT(?,'%') OR cname LIKE CONCAT(?,'%')",(className,className))
        finalDate = ""
        for final in cursor:
            finalDate = final
        finalDate = parseFinalDate(finalDate[0])
        print(finalDate)
        return f"The final exam for {className} will be on {finalDate}"
    elif(intent == "show_classes"):
        pass
    elif(intent == "textbook"):
        return "Here are the textbooks you will need for " + className
    elif(intent == "class_time"):
        cursor.execute("select unique location, day, period from class where ccode LIKE CONCAT(?,'%') OR cname LIKE CONCAT(?,'%')",(className,className))
        for (location,day,period) in cursor:
            period = str(int(period))
            string = f"{className} meets {getDays(day)} {classPeriods[str(period)]} on {location}"
            return string

    return ""




def init():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)     # setting up new voice rate
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[1].id)
    intent = None
    className = None
    while(intent != "Bye"):
        text = textInput()
        response = client.message(text)

        if(response["entities"]):
            className = str(response["entities"]["class_name:class_name"][0]["value"])

        intent = response["intents"][0]["name"]
        tts = gTTS(text=getResponse(intent,className), lang="en")
        tts.save("response.mp3")
        os.system("response.mp3")
        # engine.say(getResponse(intent,className))
        # engine.runAndWait()



init()
