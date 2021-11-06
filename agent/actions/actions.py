# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re, json
from random import randint
from . import dbconnect
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCourses(Action):

    def name(self) -> Text:
        return "action_get_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        ctype = tracker.get_slot('course_type')
        if ctype == 'cst':
            if level == 'undergrad':
                ctype = 'cis4930'
            else:
                ctype = 'cis6930'
        courses = {}
        for course in dbconnect.getCourses(ctype):
            print(course)
            if ctype == 'cis' and (course[0] == 'CIS4930' or course[0] == 'CIS6930'):
                continue
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = list(course)
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = list(course)
            
        m = ""
        cval = []
        keys = []
        if courses == {} :
            m = f"no {ctype} courses"
        else:
            cval = list(courses.values())
            keys = [*courses.keys()]
            m = ", ".join([i[1] for i in cval])
            if len(cval) > 3:
                m = ", ".join([i[1] for i in cval[:3]])
                m += f" and {len(cval) - 3} other {level} {ctype} courses in Spring 2022"
        message = f"The CISE department is offering {m} "
        for c in cval:
            message += f"=={c[0]} - {c[1]}"
        dispatcher.utter_message(message)
        # dispatcher.utter_message(json_message= json.dumps(courses))
        if len(keys) == 1:
            return [SlotSet("course", keys[0])]
        
class ActionGetCourseInfo(Action):

    def name(self) -> Text:
        return "action_get_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        c = tracker.get_slot('course')
        courses = {}
        for course in dbconnect.getCourseInfo(c):
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = course[2]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = course[2]
        message = courses
        if len(courses) == 1:
            for k in courses:
                message = f"{k} {courses[k]}"
        dispatcher.utter_message(message)
        
class ActionGetCourseInst(Action):

    def name(self) -> Text:
        return "action_get_course_inst"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        c = tracker.get_slot('course')
        courses = {}
        for course in dbconnect.getClassInst(c):
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = course[2]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = course[2]
        message = "Multiple Courses Found!"
        if len(courses) == 1:
            for k in courses:
                message = f"Professor {courses[k]} will be teaching {k} "
                if randint(1, 10) > 5:
                    message = f"{k} will be taught by {courses[k]}"
        dispatcher.utter_message(message)
        
class ActionGetCourseText(Action):

    def name(self) -> Text:
        return "action_get_course_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        c = tracker.get_slot('course')
        courses = {}
        for course in dbconnect.getCourseText(c):
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = course[2]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = course[2]
        message = "Multiple Courses Found!"
        if len(courses) == 1:
            for k in courses:
                message = f"There are no required textbooks for {k}"
                if randint(1, 10) > 5:
                    message = f"You wont need any textbooks for {k}"
        dispatcher.utter_message(message)
        
class ActionGetCourseTime(Action):

    def name(self) -> Text:
        return "action_get_course_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        c = tracker.get_slot('course')
        courses = {}
        for course in dbconnect.getClassTime(c):
            if (level == 'grad' and int(re.sub('\D', '', course[0])) > 5000) or (level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000): 
                if course[0] in courses:
                    courses[course[0]].append(list(course))
                else:
                    courses[course[0]] = [list(course)]

        message = "Multiple Courses Found!" 
        if len(courses) == 1:
            for k in courses:
                c = courses[k][0]
                message = f"{c[0]} will be taught on {c[4]} from {str(c[2])[:-3]} to {str(c[3])[:-3]} in {c[5]}"
                # for c in courses[k][1:]:
                #     message += f" and on {c[4]} from {str(c[2])[:-3]} to {str(c[3])[:-3]} in {c[5]}"
        dispatcher.utter_message(message)
        
class ActionGetCoursePreq(Action):

    def name(self) -> Text:
        return "action_get_course_preq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        c = tracker.get_slot('course')
        courses = {}
        for course in dbconnect.getCoursePreq(c):
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = course[2]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = course[2]
        message = "Multiple Courses Found!"
        if len(courses) == 1:
            for k in courses:
                message = f"{courses[k]} "
        dispatcher.utter_message(message)
        
class ActionFilterCourseInst(Action):

    def name(self) -> Text:
        return "action_filter_course_inst"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = tracker.get_slot('course_level')
        c = tracker.get_slot('faculty')
        courses = {}
        for course in dbconnect.getCoursesByInst(c):
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[2]] = course[1]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[2]] = course[1]
        message = ", ".join([*courses.values()])
        message = f"{c} will be teaching {message}"
        dispatcher.utter_message(message)
