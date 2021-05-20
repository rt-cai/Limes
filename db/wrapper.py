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
tableNames = ['sm', 'med', 'lrg']
ex = 2
# for table in tableNames:
#     cmd = 'CREATE TABLE IF NOT EXISTS %s (ID INTEGER PRIMARY KEY AUTOINCREMENT, val TEXT)' % table
#     cur.execute(cmd)
#     for i in range(10 ** ex):
#         cur.execute('INSERT INTO %s (val) VALUES ("val - %s")' % (table, i))
#     print(10 ** ex)
#     ex += 2
con.commit()
ex = 2
print('----')
for table in tableNames:
    print(table)
    for i in range(10000):
        id = genRand(10 ** ex)
        cur.execute('SELECT * FROM %s WHERE ID = %s' %(table, id))
    print(table)
    ex += 2
    

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