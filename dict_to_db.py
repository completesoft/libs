import sqlite3
import sys, os

DB_LITE = 'counter.db'
TABLE_LITE = 'counter'

def to_sqlite(DB="", TABLE="", DATA={}):
    DB = DB or DB_LITE
    Table = TABLE or TABLE_LITE

    CreateTemplate = "CREATE TABLE IF NOT EXISTS {} ".format(Table)+"(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)"
    InsertTemplate = "INSERT INTO {} ".format(Table)+"({}) values({})"
    tempAlterReal = "ALTER TABLE {} ".format(Table)+"ADD COLUMN '{}' 'REAL';"
    tempAlterText = "ALTER TABLE {} ".format(Table)+"ADD COLUMN '{}' 'TEXT';"

    if not os.access(DB, os.F_OK):
        with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute(CreateTemplate)
            cur.close()
    con = sqlite3.connect(DB)
    cursor = con.cursor()
    cursor.execute('pragma table_info(counter)')
    names = [column[1] for column in cursor.fetchall()]
    print(names)
    con.commit()

    scriptAlter = ""
    fields = ""
    data = ""
    for k, v in DATA.items():
        tempAlter = tempAlterReal
        if k not in names:
            if type(v)==str: tempAlter = tempAlterText
            scriptAlter+=tempAlter.format(k)
        fields+=k+","
        if type(v)==str:
            data += "{" + k +"!r"+ "},"
        else:
            data+="{"+k+"},"
    cursor.executescript(scriptAlter)
    con.commit()

    fields = fields[:-1]
    data = data[:-1]

    scriptInsert = InsertTemplate.format(fields, data)
    scriptInsert = scriptInsert.format(**DATA)
    print(scriptInsert)
    if not DATA:
        print("Nothing to INSERT. DATA dict empty!!!")
        sys.exit(1)
    cursor.execute(scriptInsert)
    con.commit()


if __name__=="__main__":
    to_sqlite(DB='', TABLE='', DATA={})

