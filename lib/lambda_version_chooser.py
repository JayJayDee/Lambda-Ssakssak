from typing import TypedDict
from typing_extensions import Unpack
from lib.lambda_version_mapper import LambdaVersionMapper

class Constructor(TypedDict):
    versions: list[LambdaVersionMapper]
    
class LambdaVersionChooser():

    def __init__(self, **kargs: Unpack[Constructor]):
        self.__versions = kargs['versions']

    def choose(self):
        pass
