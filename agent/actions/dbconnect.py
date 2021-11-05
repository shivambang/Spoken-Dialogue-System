import mariadb
connection = mariadb.connect(user='shiv', password='bang', database='soc', host='localhost')
cursor = connection.cursor()

def getCourses(code):
    cursor.execute("SELECT code, name, info FROM course WHERE code LIKE CONCAT(?, '%')", (code.replace(' ', ''), ))
    return [(code, name, info) for code, name, info in cursor]

def getCourseInfo(course):
    cursor.execute("SELECT code, name, info FROM course WHERE code LIKE ? OR name LIKE CONCAT('%', ?, '%')", (course.replace(' ', ''), course))
    return [(code, name, info) for code, name, info in cursor]

def getCoursePreq(course):
    cursor.execute("SELECT code, name, preq FROM course WHERE code LIKE ? OR name LIKE CONCAT('%', ?, '%')", (course.replace(' ', ''), course))
    return [(code, name, preq) for code, name, preq in cursor]

def getCourseText(course):
    cursor.execute("SELECT code, name, text FROM course WHERE code LIKE ? OR name LIKE CONCAT('%', ?, '%')", (course.replace(' ', ''), course))
    return [(code, name, text) for code, name, text in cursor]

def getClassInst(course):
    cursor.execute("SELECT DISTINCT ccode, cname, instructor FROM class WHERE ccode LIKE ? OR cname LIKE CONCAT('%', ?, '%')", (course.replace(' ', ''), course))
    return [(ccode, cname, instructor) for ccode, cname, instructor in cursor]

def getClassTime(course):
    cursor.execute("SELECT DISTINCT ccode, cname, btime, etime, day, location FROM class WHERE ccode LIKE ? OR cname LIKE CONCAT('%', ?, '%')", (course.replace(' ', ''), course))
    return [(ccode, cname, btime, etime, day, location) for ccode, cname, btime, etime, day, location in cursor]

def getCoursesByInst(inst):
    cursor.execute("SELECT DISTINCT ccode, cname, instructor FROM class WHERE instructor LIKE CONCAT('%', ?, '%')", (inst, ))
    return [(ccode, cname, instructor) for ccode, cname, instructor in cursor]

def getCoursesBefore(time):
    pass

def getCoursesAfter(time):
    pass

def getCoursesBW(start, stop):
    pass
