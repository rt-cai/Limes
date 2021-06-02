from typing import Dict, List, Tuple


class Serializable:
    def __init__(self, string: str) -> None:
        self._deserialize(string)

    # enforce string constructor
    def _deserialize(self, string: str) -> None:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    def _formatObject(self, string: str) -> Dict[str, str]:
        # print(string)
        i = 1
        parsed = {}
        q = '"'

        def next():
            nonlocal i
            i = string.find(q, i) + 1
            return i - 1

        while True:
            kl = next() + 1
            if kl == 0:
                break
            kr = next()
            vl = next() + 1
            vr = next()
            parsed[string[kl:kr]] = string[vl:vr]
        return parsed

    def _formatList(self, string: str) -> List[str]:
        i = 1
        parsed = []
        q = '"'

        def next():
            nonlocal i
            i = string.find(q, i) + 1
            return i - 1

        while True:
            l = next() + 1
            if l == 0:
                break
            r = next()
            parsed.append(string[l:r])
        return parsed