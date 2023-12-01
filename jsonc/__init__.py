r"""JSONC DOCS GO BRRRRRR"""

__version__ = '0.0.0'
__author__ = "HarryF1204"
__all__ = ["dump", "dumps", "load", "loads"]

from ._decoder import _JsonCDecoder
from ._encoder import _JsonCEncoder
import json
import os

jsonCDecoder = _JsonCDecoder()
jsonCEncoder = _JsonCEncoder()


def dump(jsonData, filePath, ensure_ascii=True, indent=2):
    """Dump formatted JSON(C) code to file
    This will delete all present text in the file.
    """

    if type(jsonData) == dict:
        jsonData = json.dumps(jsonData, indent=0, ensure_ascii=ensure_ascii)
    else:
        raise Exception(f"Incorrect data format handed to dump, Type: {type(jsonData)}")

    if os.path.exists(filePath):
        with open(filePath, 'w') as file:
            file.write(jsonCDecoder.JsonToJsonC(jsonData, tabwidth=indent))
    else:
        raise Exception(f"file not found")


def dumps(jsonData, ensure_ascii=False, tab_width=2):
    """Dump formatted JSON(C) code"""
    if type(jsonData) == dict:
        jsonData = json.dumps(jsonData, indent=0, ensure_ascii=ensure_ascii)
    else:
        raise Exception(f"Incorrect data format handed to dumps, Type: {type(jsonData)}")

    return jsonCDecoder.JsonToJsonC(jsonData, tabwidth=tab_width)


def load(filePath):
    """Load jsonc from a file to python dictionary"""
    if os.path.exists(filePath):
        with open(filePath, 'r') as file:
            jsonData = file.read()

        sJsonData = jsonCEncoder.JsonCToJson(jsonData)
        return json.loads(sJsonData)
    else:
        pass


def loads(jsonCData):
    """"""
    sJsonData = jsonCEncoder.JsonCToJson(jsonCData)
    return json.loads(sJsonData)



