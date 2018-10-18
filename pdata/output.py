import sqlite3
import xlwt
conn = sqlite3.connect('./elasticsearchDiff.db')
curs = conn.cursor()

file = xlwt.Workbook()
table = file.add_sheet("first")

curs.execute("select * from patchtable")

i = 0
for line in curs.fetchall():
    for j in range(3):
        table.write(i, j, line[j])
    i = i + 1
    name = line[2] + ".patch"
    with open("patch/" + name, 'w', encoding='utf-8') as f:
        f.write(line[3])

file.save("demo.xls")
curs.close()
conn.close()

