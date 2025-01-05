from typing import TypedDict
from typing_extensions import Unpack

class AWSAccessorFactoryOptions(TypedDict):
    dry_run: bool
    force_delete: bool

def aws_accessor_factory():
    def lambda_getter():
        pass

    return {
        'lambda': lambda_getter,
    }
