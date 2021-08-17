# from basic import AdvancedEnum, AbbreviatedEnum
# from __future__ import annotations

# # for sorting out where added data items go
# # not in use

# class Type:
#     def __init__(self, name: str, lineage: list[str] = []):
#         self.name = name
#         self.lineage = lineage

#     def __str__(self) -> str:
#         if len(self.lineage) > 0:
#             return '%s.%s' % ('.'.join(self.lineage), self.name)
#         else:
#             return self.name

#     def _eq(self, other: Type) -> bool:
#         return self.name == other.name or \
#             (self.name in other.lineage)

#     def Equals(self, other: Type | Types) -> bool:
#         if isinstance(other, Type):
#             return self._eq(other)
#         else:
#             return self._eq(other.Type)
        

# class Types(AdvancedEnum):
#     ALL = 1, Type('All')

#     def __init__(self, _:int, type: Type) -> None:
#         self.Type = type

#     def __str__(self) -> str:
#         return str(self.Type)

#     def Equals(self, other: Type | Types) -> bool:
#         return self.Type.Equals(other)
