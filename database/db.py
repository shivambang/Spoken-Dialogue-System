import re
import mariadb
import csv

def num(k):
    try:
        k = int(k)
        return k
    except ValueError:
        return 0
connection = mariadb.connect(user='shiv', password='bang', database='soc', host='localhost')
cursor = connection.cursor()
books = {}
courses = []
classes = []
with open('textbooks.csv', 'r') as inp:
    csv_inp = csv.reader(inp)
    next(csv_inp, None)
    for row in csv_inp:
        books[row[0]] = row[1:]
text = ''

p = "(?P<code>[A-Z0-9]{7,8}) - (?P<name>.+?)\n(?P<info>.+?)\n(?P<preq>(Pre|Co)req: .+?)?\n?(?P<classes>(Class #[\s\S]*?Class Dates\n.*?\n)+)"
c = re.compile("Class #(?P<num>.+?)\n(?P<days>[MTWRF][\s\S]*?\n)Textbooks[\s\S]+?Instructors?\n(?P<inst>.+?)\n[\s\S]+?Credits?\n(?P<credits>\d)\n[\s\S]+?Final Exam\n(?P<final>.+?)\nClass Dates\n(?P<date>.+?)\n")
d = re.compile("(?P<day>[MTWRF][,MTWRF]*)\s\|\s\nPeriods?\s(?P<period>.+?)\n\((?P<btime>.+?[AP]M) - (?P<etime>.+?[AP]M)\)\n(?P<loc>.+?)\n")

with open('fsoc.txt', 'r', encoding='utf-8') as f:
    text = f.read()
for course in re.finditer(p, text):
    name = re.sub('[^A-Za-z0-9]', ' ', course['name'])
    name = re.sub('Special Topics in CISE?', '', name).replace('\w+', '\w').strip()
    text = ''
    isbn = ''
    if course['code'] in books:
        isbn = books[course['code']][0]
        text = books[course['code']][1]
    elif course['code']+name in books:
        isbn = books[course['code']+name][0]
        text = books[course['code']+name][1]
    courses.append((course['code'], name, course['info'], course['preq'], text, isbn, 'N22'))
cursor.executemany("INSERT IGNORE INTO course(code, name, info, preq, text, isbn, last) VALUES (?, ?, ?, ?, ?, ?, ?)", courses)

courses = []
classes = []
with open('soc.txt', 'r', encoding='utf-8') as f:
    text = f.read()
for course in re.finditer(p, text):
    name = re.sub('[^A-Za-z0-9]', ' ', course['name'])
    name = re.sub('Special Topics in CISE?', '', name).replace('\w+', '\w').strip()
    text = ''
    isbn = ''
    if course['code'] in books:
        isbn = books[course['code']][0]
        text = books[course['code']][1]
    elif course['code']+name in books:
        isbn = books[course['code']+name][0]
        text = books[course['code']+name][1]
    courses.append((course['code'], name, course['info'], course['preq'], text, isbn, 'S22'))
    for sect in re.finditer(c, course['classes']):
        for day in re.finditer(d, sect['days']):
            btime = day['btime'].replace(' AM', '')
            etime = day['etime'].replace(' AM', '')
            def t4(time):
                if 'PM' in time:
                    time = time.replace(' PM', '')
                    time = re.split(':', time)
                    time = [int(x) for x in time]
                    time[0] = (time[0] % 12) + 12
                    time = ":".join([str(x) for x in time])
                return time
            btime = t4(btime)
            etime = t4(etime)
            classes.append((num(sect['num']), course['code'], name, sect['inst'], day['loc'], day['day'].replace(',', ''), btime, etime, sect['final']))

prof = []
with open('ratings.csv', 'r') as inp:
    csv_inp = csv.reader(inp)
    next(csv_inp, None)
    for row in csv_inp:
        prof.append(row)

with open('courses.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['code', 'name', 'info', 'preq', 'text', 'isbn', 'last'])
    csv_out.writerows(courses)

with open('soc.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['num', 'code', 'name', 'inst', 'loc', 'day', 'period', 'final'])
    csv_out.writerows(classes)

cursor.executemany("INSERT INTO course(code, name, info, preq, text, isbn, last) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE last='S22'", courses)
cursor.executemany("INSERT INTO class(number, ccode, cname, instructor, location, day, btime, etime, final) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", classes)
cursor.executemany("INSERT INTO prof(name, rate) VALUES (?, ?)", prof)

connection.commit()
cursor.close()
connection.close()
