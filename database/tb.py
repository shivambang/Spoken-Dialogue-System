import re
import csv

books = []
with open('ref_textbook.csv', 'r') as inp:
    csv_inp = csv.reader(inp)
    next(csv_inp, None)
    for row in csv_inp:
        if row[1] != 'N/A':
            name = ''
            if row[4]:
                name = re.sub('[^A-Za-z0-9]', ' ', row[4]).replace(row[0], '')
                name = re.sub('Special Topics in CISE?', '', name).replace('\w+', '\w')
            text = row[2]
            if row[3]:
                text += ' by ' + row[3]
            books.append([row[0]+name.strip(), row[1], text])

with open('textbooks.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['code', 'isbn', 'text'])
    csv_out.writerows(books)