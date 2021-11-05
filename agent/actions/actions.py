# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re, json
from . import dbconnect
from typing import Any, Text, Dict, List

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
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = course[1]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = course[1]
        m = ""
        if courses == {} :
            m = f"no {ctype} courses"
        else:
            cval = [*courses.values()]
            m = " ".join(cval)
            if len(cval) > 3:
                m = ", ".join(cval[:3])
                m += f" and {len(cval) - 3} other {level} {ctype} courses in Spring 2022"
        message = f"The CISE department is offering {m}"
        dispatcher.utter_message(message)
        dispatcher.utter_message(json_message= json.dumps(courses))
        
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
        message = "Multiple Courses Found!"
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
            if level == 'grad' and int(re.sub('\D', '', course[0])) > 5000: 
                courses[course[0]] = course[2]
            if level == 'undergrad' and int(re.sub('\D', '', course[0])) < 5000: 
                courses[course[0]] = course[2]
        message = "Multiple Courses Found!"
        if len(courses) == 1:
            for k in courses:
                message = f"{courses[k]} will be taught on {k} "
                message = f"{k} will be taught by {courses[k]}"
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
        