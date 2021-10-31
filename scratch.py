from enum import Enum
from io import BufferedReader, FileIO
import os
# from limes_common.models.basic import AdvancedEnum
from requests import Response
import json

# class A:
#     @classmethod
#     def _dec(cls, x):
#         print(self)
#         print(x)

#     @_dec
#     def fn(self):
#         print('fn')
# x = [1, 2 , 3]
# x.reverse()
# # print(x.reverse())
# print(x)

# class Model:
#     def __init__(self, res: Response) -> None:
#         self.Code = res.status_code
#         self.data: dict = json.loads(res.text) if self.Code==200 else {}

# class Model:
#     def __init__(self, d: dict) -> None:
#         print(self.__dict__)

# class DM(Model):
#     def __init__(self, d: dict) -> None:
#         self.a:str = ''
#         super().__init__(d)

# DM({})


import secrets
x = secrets.token_urlsafe(64)
print(x)
# def BE(x):
#     x()
#     return x

# @BE
# def fn():
#     print('b')



# x: BufferedReader = open('setup.sh', 'rb')
# print(type(x))

# print(os.getpid())
# print(os.getppid())
# print(list(map(str, E)))
# for e in E:
#     print(type(e))

# from json import JSONEncoder, dumps
# import requests as py_requests
# from requests.sessions import Request
# from models.network import JsonResponse
# from common.config import ActiveClient as Config
# from datetime import datetime
# from models.network import Endpoints, HttpMethod

# import limes_provider

# time = '2021-03-04T16:24:24Z'
# o = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
# # print(o)

# x = Endpoints.REGISTER
# print(x)


# limes_provider.AddEndpoint('test', HttpMethod.GET, lambda r: JsonResponse({'from': 'le fosDB (scratch.py)'}))
# limes_provider.Start()


# SAMPLE_ID = 1
# PATH_TO_FILE = 2

# import limes

# limes.Login()
# data = limes.Get(SAMPLE_ID)
# data.Add(PATH_TO_FILE)

# import numpy as np
# x = np.load('hits.npy', allow_pickle=True)
# print(x)

# print('hgfvbndlirjldivj987654321'[-9:]s
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
