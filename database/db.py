import re
import mariadb

def num(k):
    try:
        k = int(k)
        return k
    except ValueError:
        return 0
connection = mariadb.connect(user='shiv', password='bang', database='soc', host='localhost')
cursor = connection.cursor()

text = ''
with open('soc.txt', 'r', encoding='utf-8') as f:
    text = f.read()

p = "(?P<code>[A-Z0-9]{7,8}) - (?P<name>.+?)\n(?P<info>.+?)\n(?P<preq>(Pre|Co)req: .+?)?\n?(?P<classes>(Class #[\s\S]*?Class Dates\n.*?\n)+)"
c = re.compile("Class #(?P<num>.+?)\n(?P<days>[MTWRF][\s\S]*?)\nTextbooks[\s\S]+?Instructors?\n(?P<inst>.+?)\n[\s\S]+?Credits?\n(?P<credits>\d)\n[\s\S]+?Final Exam\n(?P<final>.+?)\nClass Dates\n(?P<date>.+?)\n")
d = re.compile("(?P<day>[MTWRF][,MTWRF]*)\s\|\s\nPeriods?\s(?P<period>.+?)\n\(.+?\)\n(?P<loc>.+?)\n")
courses = []
classes = []
for course in re.finditer(p, text):
    courses.append((course['code'], course['name'], course['info'], course['preq'], 'S22'))
    for sect in re.finditer(c, course['classes']):
        for day in re.finditer(d, sect['days']):
            classes.append((num(sect['num']), course['code'], course['name'], sect['inst'], day['loc'], day['day'].replace(',', ''), day['period'], sect['final']))

print(courses)
print(classes)
cursor.executemany("INSERT INTO course(code, name, info, preq, last) VALUES (?, ?, ?, ?, ?)", courses)
cursor.executemany("INSERT INTO class(number, ccode, cname, instructor, location, day, period, final) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", classes)


connection.commit()
cursor.close()
connection.close()