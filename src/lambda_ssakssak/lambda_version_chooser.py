from datetime import datetime
from typing import TypedDict
from typing_extensions import Unpack
from lambda_version_mapper import LambdaVersionMapper

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

    def mark_deleted_all(self):
        for version in self.__versions:
            if version.is_can_be_mark_as_deleted():
                version.mark_as_deleted()

    def mark_deleted_after(self, d_after: datetime):
        """
        """
        # TODO: mark version after d_after as a deleted

    def mark_deleted_in_duration(self, d_from: datetime, d_to: datetime):
        pass