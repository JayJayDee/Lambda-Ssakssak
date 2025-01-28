from datetime import datetime
from typing import TypedDict
from typing_extensions import Unpack
from lib.lambda_version_mapper import LambdaVersionMapper

class Constructor(TypedDict):
    versions: list[LambdaVersionMapper]
    
class LambdaVersionChooser():

    def __init__(self, **kargs: Unpack[Constructor]):
        self.__versions = kargs['versions']
    
    def mark_retain_latest(self):
        """
        Mark lastest versions are not be deleted. (this option should be default)
        """
        for version in self.__versions:
            if version.is_latest_version():
                version.mark_as_retain()

    def choose_with_duration(self, d_from: datetime, d_to: datetime):
        pass
