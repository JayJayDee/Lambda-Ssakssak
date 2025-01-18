from typing import TypedDict, Literal
from typing_extensions import Unpack
from mypy_boto3_lambda import type_defs
import arn_validators

LambdaVersionStatus = Literal['uninspected', 'has_deps', 'has_no_deps']

class Constructor(TypedDict):
    lambda_arn: str
    version: str
    status: LambdaVersionStatus

class LambdaVersionMapper:

    def __init__(self, **kargs: Unpack[Constructor]):
        self._lambda_arn = kargs['lambda_arn']
        self._version = kargs['version']
        self._status = kargs['status']
        arn_validators.ensure_valid_version_arn()

    def str(self):
        return f'LambaVersion({self._lambda_arn}:{self._version})'
    
    def is_latest_version(self):
        if self._version == '$LATEST':
            return True
        return False

    @classmethod
    def from_boto3_response(cls, funcdef: type_defs.FunctionConfigurationTypeDef):
        """
        make LambdaVersion instances from boto3 response
        """
        version = LambdaVersionMapper(
            lambda_arn=funcdef['FunctionArn'],
            version=funcdef['Version'],
            status='uninspected'
        )
        return version
