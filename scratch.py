from json import JSONEncoder, dumps

from common.data import Sample

s = Sample({'Name': 'gar'})
s.Name
print(s.G)

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
