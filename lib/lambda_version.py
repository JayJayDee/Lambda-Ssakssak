from typing import TypedDict, Literal
from typing_extensions import Unpack
from aws_client_factory import aws_client

LambdaVersionStatus = Literal['uninspected', 'has_deps', 'has_no_deps']

class Constructor(TypedDict):
    version_arn: str
    status: LambdaVersionStatus

class LambdaVersionNotationInvalidException(Exception):
    pass

class LambdaVersion:

    def __init__(self, **kargs: Unpack[Constructor]):
        self._version_arn = kargs['version_arn']
        self._status = kargs['status']

    @classmethod
    def from_lambda_arn(lambda_arn: str):
        """
        make LambdaVersion instances from lambda arn string
        """
        aws_client('lambda')
        pass

    @staticmethod
    def ensure_valid_lambda_arn(lambda_arn: str):
        """
        Ensures given lambda  arn expression is valid (note: not a VERSION ARN)
        """
        is_start_with_arn = lambda_arn.startswith('arn:aws:lambda')
        if not is_start_with_arn:
            raise LambdaVersionNotationInvalidException('not a valid lambda arn')

    @staticmethod
    def ensure_valid_version_arn(version_arn: str):
        """
        Ensures given lambda version arn expression is valid (note: not a LAMBDA ARN)
        """
        LambdaVersion.ensure_valid_lambda_arn(version_arn)
        splited_with_colon = version_arn.split(':')
        is_end_with_vernum = splited_with_colon[-1].isnumeric()    
        if not is_end_with_vernum:
            raise LambdaVersionNotationInvalidException('not a valid lambda version arn.')
