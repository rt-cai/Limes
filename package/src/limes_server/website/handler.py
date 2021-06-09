# from limes_common.models.network import ErrorResponse, Request, Response, ContentType
# import os
# from limes_common.models.basic import AbbreviatedEnum, AdvancedEnum
# from typing import Callable

# _PARENT_FOLDER = 'website'

# class Pages(AbbreviatedEnum):
#     HOME = 1
#     SLEEP = 2

#     def __init__(self, i: int) -> None:
#         self.GetPage: Callable[[], str] = lambda: self._load(str(Pages(i)))

#     def _load(self, file: str):
#         return open('%s/public/%s.html' % (_PARENT_FOLDER, file.title())).read()

# def ServeFolder() -> Callable[[Request], Response]:
#     def fn(req: Request) -> Response:
#         allowedTypes = {
#             '.css': ContentType.CSS,
#             '.js': ContentType.JAVASCRIPT,
#             '.png': ContentType.PNG
#         }
#         rType = None
#         for k, v in allowedTypes.items():
#             if req.Path.endswith(k):
#                 rType = v
#         if rType is None:
#             return ErrorResponse(404, ContentType.HTML, 'no such file [%s]' % req.Path)
#         else:
#             if rType == ContentType.PNG:
#                 res = Response(200, rType, '')
#                 res.Bytes = open('%s%s' % (_PARENT_FOLDER, req.Path), 'rb').read()
#                 return res
#             else:
#                 return Response(200, rType, open('%s%s' % (_PARENT_FOLDER, req.Path)).read())
#     return fn