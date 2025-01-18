from typing import TypedDict, NotRequired
from typing_extensions import Unpack
from lambda_version_mapper import LambdaVersionMapper
from mypy_boto3_lambda import type_defs
from boto3_type_annotations.lambda_ import LambdaClient
import arn_validators

class Constructor(TypedDict):
    lambda_arn: str
    client: LambdaClient

class LambdaNotationInvalidException(Exception):
    pass

class LambdaMapper:

    def __init__(self, **kargs: Unpack[Constructor]):
        self._lambda_arn = kargs['lambda_arn']
        self._client = kargs['client']
        arn_validators.ensure_valid_lambda_arn(self._lambda_arn)

    def str(self):
        return f'LambdaMapper({self._lambda_arn})'
    
    def populate_versions(self) -> list[LambdaVersionMapper]:

        return 

    @classmethod
    def from_boto3_response(cls, funcdef: type_defs.FunctionConfigurationTypeDef):
        """
        make LambdaVersion instances from boto3 response
        """
        version = LambdaMapper(
            lambda_arn=funcdef['FunctionArn'],
        )
        return version
