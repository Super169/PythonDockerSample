import re


class RE:
    @staticmethod
    def getFirst(data: str, pattern: str, default: str = '') -> str:
        result = re.findall(pattern, data)
        if result is None or len(result) == 0:
            return default
        return result[0]

    @staticmethod
    def cleanResult(data: str) -> str:
        if data is None:
            return ''
        data = re.sub(r'\r\n', ' ', data)
        data = re.sub(r'\t', ' ', data)
        data = re.sub(r' [ ]+', ' ', data)
        return data.strip()

