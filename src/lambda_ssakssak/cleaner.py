from typing import TypedDict
from typing_extensions import Unpack

class LambdaCleanOptions(TypedDict):
    dry_run: bool
    force_delete: bool

def run_cleaner(**kargs: Unpack[LambdaCleanOptions]):
    dry_run = kargs['dry_run']
    force_delete = kargs['force_delete']
    pass
