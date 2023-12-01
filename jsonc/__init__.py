r"""JSONC DOCS GO BRRRRRR"""

__version__ = '0.0.0'
__author__ = "HarryF1204"
__all__ = ["dump", "dumps", "load", "loads"]

from jsonc.decoder import JsonCDecoder
from jsonc.encoder import JsonCEncoder

import json

jsonCDecoder = JsonCDecoder()
jsonCEncoder = JsonCEncoder()


def dump():
    """Dump formatted JSON(C) code to file"""
    pass


def dumps(jsonData):
    """Dump formatted JSON(C) code"""
    if type(jsonData) == dict:
        jsonData = json.dumps(jsonData, indent=0)
    else:
        raise Exception(f"Incorrect data format handed to dumps, Type: {type(jsonData)}")

    return jsonCDecoder.JsonToJsonC(jsonData)


def load():
    """Load jsonc from a file to python dictionary"""
    pass


def loads(jsonCData):
    """"""
    sJsonData = jsonCEncoder.JsonCToJson(jsonCData)
    return json.loads(sJsonData)



