from wit import Wit
import pyttsx3


client = Wit("KADJWIX3VLFUEXI6DD5GFNWMVWI6FZBV")


# while True:
#     message = str(input("Enter your message: "))
#     resp = client.message(message)
#     print(resp)




def textInput():
    return str(input("Please enter your text: "))

def getResponse(intent, className):
    if(intent == "professor"):
        return "Professor Boyer will be teaching " + className
    elif(intent == "class_info"):
        return className + " covers the technical aspects of how neural networks work and machine learning techniques."
    elif(intent == "final_exam"):
        return "The final exam for " + className + " will be on Monday, December 18 at 10:30"
    elif(intent == "show_classes"):
        pass
    elif(intent == "textbook"):
        return "Here are the textbooks you will need for " + className
    elif(intent == "class_time"):
        return className + " meets Tuesday and Thursdays from ten 10:30am to 11:40am"




def init():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)     # setting up new voice rate
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[33].id)
    intent = None
    className = None
    while(intent != "Bye"):
        text = textInput()
        response = client.message(text)

        if(response["entities"]):
            className = str(response["entities"]["class_name:class_name"][0]["value"])

        intent = response["intents"][0]["name"]
        engine.say(getResponse(intent,className))
        engine.runAndWait()



init()
