from typing import TypedDict
from typing_extensions import Unpack
from mypy_boto3_lambda import type_defs, LambdaClient
from lib import arn_validators

class Constructor(TypedDict):
    lambda_arn: str

class LambdaMapper:

    def __init__(self, **kargs: Unpack[Constructor]):
        self._lambda_arn = kargs['lambda_arn']
        arn_validators.ensure_valid_lambda_arn(self._lambda_arn)

    def str(self):
        return f'LambdaMapper({self._lambda_arn})'
    
    @classmethod
    def fetch_all(cls, client: LambdaClient):
        next_marker: str | None = None
        fetched_all_lambdas: list[cls] = []

        while True:
            response = client.list_functions(
                **({'Marker': next_marker} if next_marker is not None else {})
            )
            next_marker = response['NextMarker'] if 'NextMarker' in response else None
            raw_functions = response['Functions']
            lambdas = list(map(lambda x : cls.from_boto3_response(x), raw_functions))
            fetched_all_lambdas.extend(lambdas)

            if next_marker is None:
                break

        return fetched_all_lambdas

    @classmethod
    def from_boto3_response(cls, funcdef: type_defs.FunctionConfigurationTypeDef):
        """
        make LambdaVersion instances from boto3 response
        """
        version = cls(
            lambda_arn=funcdef['FunctionArn'],
        )
        return version
    
    @property
    def lambda_arn(self):
        return self._lambda_arn
