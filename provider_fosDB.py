from limes_provider import HttpMethod, Provider, JsonResponse
from db.wrapper import Database
import random
import math

# db = Database()

# count: int = 1000000
# slice = count / 10
# for i in range(count):
#     db.Insert('dummy val - %s' % i)
#     if i % slice == 0:
#         print('%f' % (i/count))
# db.Commit()

# random.seed(12345)
# def genRand():
#     return math.floor((random.random() * count) + 1)

# c2 = 100000
# slice = c2/10
# for i in range(c2):
#     rand = genRand()
#     res = db.Exec('SELECT * FROM asdf WHERE ID = %s' % rand)
#     if i % slice == 0:
#         for row in res:
#             print(row)
#         print('----')