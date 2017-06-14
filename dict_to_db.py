import sqlite3
import sys, os


DB_LITE = 'counter.db'

def computing(DB, dictData):
    if not os.access(DB, os.F_OK):
        with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS counter(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)")
            cur.close()
    con = sqlite3.connect(DB)
    cursor = con.cursor()
    cursor.execute('pragma table_info(counter)')
    names = [column[1] for column in cursor.fetchall()]
    print(names)
    con.commit()

    scriptAlter = ""
    InsertTemplate = "INSERT INTO counter ({}) values({})"
    fields = ""
    data = ""
    for k, v in dictData.items():
        tempAlter = "ALTER TABLE counter ADD COLUMN '{}' 'REAL';"
        if k not in names:
            scriptAlter+=tempAlter.format(k)
        fields+=k+","
        data+="{"+k+"},"

    cursor.executescript(scriptAlter)
    con.commit()

    fields = fields[:-1]
    data = data[:-1]

    scriptInsert = InsertTemplate.format(fields, data)
    scriptInsert = scriptInsert.format(**dictData)
    cursor.execute(scriptInsert)
    con.commit()


if __name__=="__main__":
    computing(DB_LITE, dictIncomeData)