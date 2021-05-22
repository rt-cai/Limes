import sqlite3 as db
import random
import math
# _provider = Provider()
# _provider.AddEndpoint('test', HttpMethod.GET, lambda r: JsonResponse({'from': 'le fosDB'}))
# _provider.Start()

random.seed(12345)
def genRand(c):
    return math.floor((random.random() * c) + 1)

con = db.connect('db/test/test_man.db')
cur = con.cursor()

table = 'vacTest'
cur.execute('CREATE TABLE %s (ID INTEGER PRIMARY KEY AUTOINCREMENT, i INTEGER, val TEXT)' % table)
count: int = 1000000
slice = count / 10
for i in range(count):
    cur.execute('INSERT INTO %s (i, val) VALUES (%s, "old - %s")' % (table, genRand(count), i))
    if i % slice == 0:
        print('%f' % (i/count))

print('del')
cur.execute('DELETE FROM %s WHERE ID < %s' % (table, 4 * count / 5))
print('/del')

print('com')
con.commit()
print('/com')

print('vac')
cur.execute('VACUUM')
print('/vac')





class Database:
    def __init__(self) -> None:
        self._PATH = 'db/test/'
        self._connection = db.connect('%stest.db' % self._PATH)

        table = 'asdf'
        cur = self._connection.cursor()
        # cur.execute('DROP TABLE IF EXISTS %s' % table)
        # cur.execute('CREATE TABLE %s (ID INTEGER PRIMARY KEY AUTOINCREMENT, val TEXT)' % table)
        self._cursor = cur

    def Insert(self, val: str):
        table = 'asdf'
        self._cursor.execute('INSERT INTO %s (val) VALUES ("%s")' % (table, val))

    def Get(self):
        table = 'asdf'
        return self._cursor.execute('SELECT * from %s' % table)

    def Exec(self, cmd):
        return self._cursor.execute(cmd)

    def Commit(self):
        self._connection.commit()

    def Close(self):
        self._connection.close()