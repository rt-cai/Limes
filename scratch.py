from json import JSONEncoder, dumps
import requests as py_requests
from common.config import ActiveClient as Config
from datetime import datetime

from common.models import Sample

time = '2021-03-04T16:24:24Z'
o = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
print(o)

# class a:

#     def test(self, x):
#         self.otherFn(self.fn, x)

#     def fn(self, x):
#         return x

#     def otherFn(self, fn, x):
#         print(fn(x))

# a().test('yo')

# def constructor(self):
#     self.y = 12
#     pass

# b = type('b', (object, ), {
#     '__init__': constructor
# })

# bb = b()
# bb.y


# s = Sample({'Name': 'gar'})
# s.Name
# print(Config.ELAB_URL)
# cred = open(Config.CREDENTIALS_PATH)
# u = cred.readline()
# p = cred.readline()
# print(u)
# print(p)


# import asyncio

# async def a():
#     await asyncio.sleep(1)
#     print('a1')

#     await asyncio.sleep(1)
#     print('a2')

# async def pa(s, m):
#     await asyncio.sleep(s)
#     print(m)

# async def main():
#     t1 = asyncio.create_task(pa(3, 'first'))
#     t2 = asyncio.create_task(pa(2, 'second'))

#     await pa(4, 'pa1')
#     print('m1')
#     await t1
#     await t2
#     print('m2')

# asyncio.run(main())
# print('o1')
